import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class UpdateProfessorPage extends StatefulWidget {
  final int professorId;
  final String firstName;
  final String lastName;
  final String email;

  const UpdateProfessorPage({super.key, 
    required this.professorId,
    required this.firstName,
    required this.lastName,
    required this.email,
  });

  @override
  State createState() => _UpdateProfessorPageState();
}

class _UpdateProfessorPageState extends State<UpdateProfessorPage> {
  String? _selectedField;
  TextEditingController _fieldController = TextEditingController();

  // Function to handle updating the professor's data
  Future<void> _updateProfessor() async {
    final Map<String, dynamic> updatedData = {
      _selectedField?? "": _fieldController.text,
    };

    final response = await http.put(
      Uri.parse('http://127.0.0.1:5000/professors/${widget.professorId}'), // Replace with your actual API URL
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(updatedData),
    );

    if (response.statusCode == 200) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Professor updated successfully!')));
      Navigator.pop(context);  // Close the dialog box
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed to update professor')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text('Update Professor'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          DropdownButton<String>(
            hint: Text('Select Field to Update'),
            value: _selectedField,
            items: [
              'first_name',
              'last_name',
              'email',
              'phone_number',
              'salary',
              'professor_number',
              'hire_date',
            ].map((field) {
              return DropdownMenuItem<String>(
                value: field,
                child: Text(field),
              );
            }).toList(),
            onChanged: (value) {
              setState(() {
                _selectedField = value;
              });
            },
          ),
          if (_selectedField != null)
            TextField(
              controller: _fieldController,
              decoration: InputDecoration(labelText: 'New Value for $_selectedField'),
            ),
        ],
      ),
      actions: [
        ElevatedButton(
          onPressed: _updateProfessor,
          child: Text('Update'),
        ),
      ],
    );
  }
}
