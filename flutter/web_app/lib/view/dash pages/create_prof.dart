import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class CreateProf extends StatefulWidget {
  const CreateProf({super.key});

  @override
  State createState() => _CreateProfState();
}

class _CreateProfState extends State<CreateProf> {
  final _formKey = GlobalKey<FormState>();

  // Controllers to handle input text
  final TextEditingController _firstNameController = TextEditingController();
  final TextEditingController _lastNameController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _hireDateController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  bool _isActive = true; // Checkbox to mark if the professor is active

  // Function to handle form submission
  Future<void> _addProfessor() async {
    final Map<String, dynamic> professorData = {
      'firstname': _firstNameController.text,
      'lastname': _lastNameController.text,
      'email': _emailController.text,
      'hire_date': _hireDateController.text,
      'password': _passwordController.text,
    };

    final response = await http.post(
      Uri.parse(
          'http://127.0.0.1:5000/professors'), // Update with your Flask URL
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(professorData),
    );

    if (response.statusCode == 201) {
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Professor added successfully!')));
      // You can navigate back or clear the form here
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text('Failed to add professor')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Add Professor')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: SingleChildScrollView(
            child: Column(
              children: [
                TextFormField(
                  controller: _firstNameController,
                  decoration: InputDecoration(labelText: 'First Name'),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter the first name';
                    }
                    return null;
                  },
                ),
                TextFormField(
                  controller: _lastNameController,
                  decoration: InputDecoration(labelText: 'Last Name'),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter the last name';
                    }
                    return null;
                  },
                ),
                TextFormField(
                  controller: _emailController,
                  decoration: InputDecoration(labelText: 'Email'),
                  keyboardType: TextInputType.emailAddress,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter the email';
                    }
                    return null;
                  },
                ),
                TextFormField(
                  controller: _hireDateController,
                  decoration: InputDecoration(labelText: 'Hire Date'),
                  keyboardType: TextInputType.datetime,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter the hire date';
                    }
                    return null;
                  },
                ),
                TextFormField(
                  controller: _passwordController,
                  decoration: InputDecoration(labelText: 'password'),
                ),
                Row(
                  children: [
                    Text('Active'),
                    Checkbox(
                      value: _isActive,
                      onChanged: (bool? value) {
                        setState(() {
                          _isActive = value!;
                        });
                      },
                    ),
                  ],
                ),
                ElevatedButton(
                  onPressed: () {
                    if (_formKey.currentState?.validate() ?? false) {
                      _addProfessor();
                    }
                  },
                  child: Text('Add Professor'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
