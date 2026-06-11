from app.database import get_connection

def row_to_dict(row):
    if row is None:
        return None
    return dict(row)

def reset_services():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM services")
    cursor.execute("DELETE from sqlite_sequence WHERE name ='services'")
    conn.commit()
    conn.close()


def create_service_record(service):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO services (name, url, owner, status) VALUES (?, ?, ?, ?)",
        (service.name, service.url, service.owner, "unknown")
    )
    conn.commit()
    service_id =cursor.lastrowid
    conn.close()
    return get_service_by_id(service_id)


def list_service_records():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM services")
    rows = cursor.fetchall()
    service_list = []
    for row in rows:
        service_list.append(row_to_dict(row))
    conn.close()
    return service_list
    

def update_service_status_record(service_id: int, status: str):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("UPDATE services SET status = ? WHERE id = ?",
                   (status, service_id))
    conn.commit()
    conn.close()
    return get_service_by_id(service_id)

def get_service_by_id(service_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM services WHERE id = ?",
        (service_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row_to_dict(row)


def delete_service_by_id(service_id: int):
    deleted_service=get_service_by_id(service_id)
    if deleted_service is None:
        return None
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM services WHERE id = ?",
                   (service_id,))
    conn.commit()
    conn.close()
    return deleted_service
    
