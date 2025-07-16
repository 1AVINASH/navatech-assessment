CREATE TABLE IF NOT EXISTS admin (
    id BIGSERIAL PRIMARY KEY,
    email text not null,
    password text not null,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_admin_email_password ON admin (LOWER(email), password);

CREATE TABLE IF NOT EXISTS organization (
    id BIGSERIAL PRIMARY KEY,
    name text UNIQUE not null,
    admin_id BIGINT REFERENCES admin(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_organization_name ON organization (LOWER(name));

ALTER TABLE organization
ADD CONSTRAINT UQ_organization_name UNIQUE (name);