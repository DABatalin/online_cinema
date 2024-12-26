CREATE OR REPLACE FUNCTION log_user_activity()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO userlogs (user_id, operation_status)
    VALUES (NEW.id, 'Вход в систему');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER log_user_login
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION log_user_activity();

