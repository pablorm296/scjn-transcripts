from pymongo import AsyncMongoClient
from redis import Redis
from math import ceil

from scjn_transcripts.models.collector.response.document import DocumentDetailsResponse
from scjn_transcripts.clients.buscador_jurídico import BuscadorJurídicoApiClient
from scjn_transcripts.models.collector.response.búsqueda import BúsquedaResponse
from scjn_transcripts.utils.mongo import MongoClientFactory
from scjn_transcripts.utils.redis import RedisFactory

import scjn_transcripts.utils.clients.buscador_jurídico as clients_utils
import scjn_transcripts.utils.digest as digest_utils

class ScjnSTranscriptsCollector:
    client: BuscadorJurídicoApiClient
    cache_client: Redis | None = None
    mongo_client: AsyncMongoClient | None = None

    def __init__(self):
        self.__init_client()

    def __init_client(self):
        self.client = BuscadorJurídicoApiClient()

    def __init_cache_client(self):
        self.cache_client = RedisFactory.create()

    def __check_cache_client(self):
        if self.cache_client is None:
            raise ValueError("Cache client not initialized")
        
    def __check_mongo_client(self):
        if self.mongo_client is None:
            raise ValueError("Mongo client not initialized")
        
    def __check_connection_clients(self):
        self.__check_cache_client()
        self.__check_mongo_client()

    def __set_search_page_in_cache(self, page: int):
        self.cache_client.set("scjn_transcripts:search_page", page)

    def __get_search_page_from_cache(self) -> int:
        page = self.cache_client.get("scjn_transcripts:search_page")
        return int(page) if page else 1
    
    def __set_document_details_in_cache(self, id: str, digest: str):
        mapping = {
            "id": id,
            "digest": digest
        }

        self.cache_client.hset(f"scjn_transcripts:document_details:{id}", mapping = mapping)

    def __check_document_details_in_cache(self, id: str) -> bool | str:
        exists = self.cache_client.exists(f"scjn_transcripts:document_details:{id}")

        if exists:
            mapping = self.cache_client.hgetall(f"scjn_transcripts:document_details:{id}")
            return mapping["digest"]
        
        return False
    
    def __check_and_set_transcript(self, document_details: DocumentDetailsResponse) -> DocumentDetailsResponse:
        # If document_details.contenido is undefined ot empty, it means that the transcript should
        # be obtained by calling the get_print method. However, we must check the result of the get_print
        # to see if the returned transcript is text or binary. If it is binary, we must skip the document.
        if not document_details.contenido:
            print_response = self.client.get_print(document_details.archivo)
            is_response_text = clients_utils.response_is_text(print_response)

            if is_response_text:
                print_text_content = print_response.text
                is_base64 = clients_utils.text_is_base64(print_text_content)

                document_details.contenido = print_text_content if not is_base64 else clients_utils.base64_to_text(print_text_content)

        return document_details
    
    async def __save_document_details_in_db(self, document_details: DocumentDetailsResponse):
        result = await self.mongo_client.db.transcripts.insert_one(document_details.model_dump())
        return result.inserted_id
    
    async def __patch_document_details_in_db(self, document_details: DocumentDetailsResponse) -> int:
        result = await self.mongo_client.db.transcripts.update_one(
            {"id": document_details.id},
            {"$set": document_details.model_dump()}
        )
        return result.modified_count

    async def __init_mongo_client(self):
        self.mongo_client = await MongoClientFactory.create()

    async def connect(self):
        """Connect to DB and cache clients.

        This method should be called before any other method that requires
        a connection to the DB or cache.

        This method should be called only once, as it initializes the
        DB and cache clients.

        This implementation is a workaround to the fact that the
        __init__ method cannot be async.
        """

        await self.__init_mongo_client()
        self.__init_cache_client()

    async def close(self):
        """Close the connection to the DB and cache clients.

        This method should be called when the application is shutting down.
        """

        self.__check_connection_clients()

        self.mongo_client.close()
        self.cache_client.close()

    async def collect(self):
        """Collect transcripts from the SCJN website.

        This method collects transcripts from the SCJN website and stores
        them in the DB.

        This method should be called after the connect method has been called.
        """

        # Check that the DB and cache clients are connected
        self.__check_connection_clients()

        # Get the search page from the cache
        page = self.__get_search_page_from_cache()
        
        # Init collector variables
        page_size = 20
        total_pages = 0
        total_items = 0
        requests = 0
        saved = 0
        patched = 0

        # Loop through the search results
        while True:
            search_response = self.client.get_búsqueda("*", index = "vtaquigraficas", page = page, size = page_size)
            parsed_search_response = BúsquedaResponse(**search_response.json())

            # If it's the first page, set the total pages
            if requests == 0:
                total_items = parsed_search_response.total
                total_pages = ceil(total_items / page_size)

            # Loop through the search results
            for item in parsed_search_response.resultados:
                # Get the document_details id
                id = item.id

                # Request the full document details
                document_response = self.client.get_documento(id)
                parsed_document_response = DocumentDetailsResponse(**document_response.json())

                # Check and set the transcript
                parsed_document_response = self.__check_and_set_transcript(parsed_document_response)

                parsed_document_response_dump = parsed_document_response.model_dump()
                parsed_document_response_digest = digest_utils.get_digest(parsed_document_response_dump)

                # Get the document digest from the cache
                digest = self.__check_document_details_in_cache(id)

                if digest:
                    # Check if the document has changed
                    if parsed_document_response_digest == digest:
                        # If the document hasn't changed, skip it
                        continue

                    # If the document has changed, patch it
                    patched += await self.__patch_document_details_in_db(parsed_document_response_dump)

                    # Update the digest in the cache
                    self.__set_document_details_in_cache(id, parsed_document_response_digest)
                else:
                    # Save the document in the DB
                    new_id = await self.__save_document_details_in_db(parsed_document_response)

                    # Save the digest in the cache
                    self.__set_document_details_in_cache(id, parsed_document_response_digest)

                    saved += 1
                
            requests += 1
            page += 1

            # Check if we've reached the total pages
            if requests >= total_pages:
                break

            # Set the search page in the cache
            self.__set_search_page_in_cache(page)

        return {
            "total_items": total_items,
            "saved": saved,
            "patched": patched
        }


if __name__ == "__main__":
    async def main():
        collector = ScjnSTranscriptsCollector()
        await collector.connect()
        result = await collector.collect()
        await collector.close()
        print(result)

    import asyncio
    asyncio.run(main())