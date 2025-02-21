// Create an admin user, so anonymous users can't access the database
db = db.getSiblingDB('admin');

db.createUser({
    user: 'admin',
    pwd: 'admin',
    roles: [
        {
            role: 'userAdminAnyDatabase',
            db: 'admin',
        },
    ],
});

// Create a user with read and write access to all databases
db.createUser({
    user: 'scjn-transcripts',
    pwd: 'password',
    roles: [
        {
            role: 'readWriteAnyDatabase',
            db: 'admin',
        },
    ],
});