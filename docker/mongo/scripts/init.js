// Create an admin user, so anonymous users can't access the database
db = db.getSiblingDB('admin');

print('Creating admin user...');
db.createUser({
    user: 'admin',
    pwd: 'CxJ7GxFyId2wj6uF',
    roles: [
        {
            role: 'userAdminAnyDatabase',
            db: 'admin',
        },
    ],
});

print('Creating app user...');
db.createUser({
    user: 'scjn-transcripts',
    pwd: 'r3nltTVCTp7oI1sZ',
    roles: [
        {
            role: 'readWriteAnyDatabase',
            db: 'admin',
        },
    ],
});