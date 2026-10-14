from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date
import database as db
import sqlite3

app = FastAPI(
    title="Student Database CRUD API",
    description="A production-ready Python backend application to manage student profiles using FastAPI and SQLite.",
    version="1.0.0"
)

# --- PYDANTIC SCHEMAS FOR INPUT VALIDATION ---

class StudentCreate(BaseModel):
    student_id: str = Field(..., description="Unique alphanumeric identifier for the student.")
    name: str = Field(..., min_length=2, description="Full name of the student.")
    dob: date = Field(..., description="Date of birth in YYYY-MM-DD format.")
    email: Optional[EmailStr] = Field(None, description="Valid student email address.")
    phone: Optional[str] = Field(None, description="Contact phone number.")
    course: Optional[str] = Field(None, description="Enrolled course name.")
    address: Optional[str] = Field(None, description="Physical residential address.")
    enrollment_date: Optional[date] = Field(default_factory=date.today, description="Date of enrollment.")

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    dob: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None

class StudentResponse(BaseModel):
    student_id: str
    name: str
    dob: date
    email: Optional[str]
    phone: Optional[str]
    course: Optional[str]
    address: Optional[str]
    enrollment_date: Optional[date]

# --- API ENDPOINTS ---

@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    """Adds a new student record to the database."""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            INSERT INTO students (student_id, name, dob, email, phone, course, address, enrollment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student.student_id,
                student.name,
                str(student.dob),
                student.email,
                student.phone,
                student.course,
                student.address,
                str(student.enrollment_date) if student.enrollment_date else None
            )
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Student with ID '{student.student_id}' already exists."
        )
    
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student.student_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)


@app.get("/students", response_model=List[StudentResponse])
def list_students(course: Optional[str] = Query(None, description="Filter students by course name")):
    """Lists all students, with an optional filter for specific courses."""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    if course:
        cursor.execute("SELECT * FROM students WHERE course LIKE ?", (f"%{course}%",))
    else:
        cursor.execute("SELECT * FROM students")
        
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.get("/students/{student_id}", response_model=StudentResponse)
def view_student(student_id: str):
    """Retrieves a single student's profile by their unique ID."""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student record with ID '{student_id}' not found."
        )
    return dict(row)


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: str, student_data: StudentUpdate):
    """Modifies details of an existing student profile."""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student record with ID '{student_id}' not found."
        )
    
    update_dict = student_data.model_dump(exclude_unset=True)
    if not update_dict:
        conn.close()
        return dict(row)
        
    set_clause = ", ".join([f"{key} = ?" for key in update_dict.keys()])
    values = [str(val) if isinstance(val, date) else val for val in update_dict.values()]
    values.append(student_id)
    
    cursor.execute(f"UPDATE students SET {set_clause} WHERE student_id = ?", tuple(values))
    conn.commit()
    
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    updated_row = cursor.fetchone()
    conn.close()
    return dict(updated_row)


@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
def delete_student(student_id: str):
    """Removes a student profile entirely from the database."""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student record with ID '{student_id}' not found."
        )
        
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
    return {"message": f"Student record with ID '{student_id}' successfully deleted."}
