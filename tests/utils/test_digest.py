from scjn_transcripts.utils.digest import check_digest, get_digest

def test_get_digest():
    data = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }
    
    data_different_order = {
        "key3": "value3",
        "key1": "value1",
        "key2": "value2"
    }

    data_different_value = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value4"
    }

    digest = get_digest(data)
    digest_different_order = get_digest(data_different_order)
    digest_different_value = get_digest(data_different_value)

    assert digest == digest_different_order
    assert digest != digest_different_value