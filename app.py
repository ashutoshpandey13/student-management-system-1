from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from datetime import datetime

app = Flask(__name__)

# In-memory storage for students (runtime only, no database)
students_db = {}
next_id = 1

# Generate encryption key (using cryptography library)
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Student API is running',
        'total_students': len(students_db)
    }), 200

# CREATE - Add a new student
@app.route('/api/students', methods=['POST'])
def create_student():
    global next_id
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['name', 'email', 'age', 'course']):
            return jsonify({'error': 'Missing required fields: name, email, age, course'}), 400
        
        # Check if email already exists
        for student in students_db.values():
            if student['email'] == data['email']:
                return jsonify({'error': 'Email already exists'}), 409
        
        # Create new student
        new_student = {
            'id': next_id,
            'name': data['name'],
            'email': data['email'],
            'age': data['age'],
            'course': data['course'],
            'enrollment_date': datetime.now().isoformat()
        }
        
        students_db[next_id] = new_student
        next_id += 1
        
        return jsonify({
            'message': 'Student created successfully',
            'student': new_student
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ - Get all students
@app.route('/api/students', methods=['GET'])
def get_all_students():
    try:
        students_list = list(students_db.values())
        return jsonify({
            'count': len(students_list),
            'students': students_list
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ - Get a specific student by ID
@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        if student_id not in students_db:
            return jsonify({'error': 'Student not found'}), 404
        
        return jsonify({'student': students_db[student_id]}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE - Update a student by ID
@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        if student_id not in students_db:
            return jsonify({'error': 'Student not found'}), 404
        
        data = request.get_json()
        student = students_db[student_id]
        
        # Update fields if provided
        if 'name' in data:
            student['name'] = data['name']
        if 'email' in data:
            # Check if new email already exists for another student
            for sid, s in students_db.items():
                if sid != student_id and s['email'] == data['email']:
                    return jsonify({'error': 'Email already exists'}), 409
            student['email'] = data['email']
        if 'age' in data:
            student['age'] = data['age']
        if 'course' in data:
            student['course'] = data['course']
        
        student['updated_at'] = datetime.now().isoformat()
        
        return jsonify({
            'message': 'Student updated successfully',
            'student': student
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE - Delete a student by ID
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        if student_id not in students_db:
            return jsonify({'error': 'Student not found'}), 404
        
        deleted_student = students_db.pop(student_id)
        
        return jsonify({
            'message': 'Student deleted successfully',
            'student': deleted_student
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Encrypt data endpoint (demonstrates cryptography usage)
@app.route('/api/encrypt', methods=['POST'])
def encrypt_data():
    try:
        data = request.get_json()
        if 'text' not in data:
            return jsonify({'error': 'Missing text field'}), 400
        
        encrypted_text = cipher_suite.encrypt(data['text'].encode())
        return jsonify({
            'original': data['text'],
            'encrypted': encrypted_text.decode(),
            'key': encryption_key.decode(),
            'note': 'Using cryptography 46.0.5 (vulnerable version)'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Decrypt data endpoint
@app.route('/api/decrypt', methods=['POST'])
def decrypt_data():
    try:
        data = request.get_json()
        if 'encrypted_text' not in data:
            return jsonify({'error': 'Missing encrypted_text field'}), 400
        
        decrypted_text = cipher_suite.decrypt(data['encrypted_text'].encode())
        return jsonify({
            'decrypted': decrypted_text.decode()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Clear all students (for testing)
@app.route('/api/students/clear', methods=['DELETE'])
def clear_all_students():
    global students_db, next_id
    count = len(students_db)
    students_db = {}
    next_id = 1
    return jsonify({
        'message': f'Cleared {count} students from memory',
        'total_students': 0
    }), 200

if __name__ == '__main__':
    # Add some sample data on startup
    print("Starting Student API with in-memory storage...")
    print("Note: All data will be lost when the container stops!")
    app.run(host='0.0.0.0', port=5000, debug=True)
