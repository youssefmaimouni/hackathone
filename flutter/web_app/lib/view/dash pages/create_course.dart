import 'package:flutter/material.dart';
import 'package:web_app/data/course_data.dart';

class CreateCourse extends StatefulWidget {
  @override
  State createState() => _CreateCourseState();
}

class _CreateCourseState extends State<CreateCourse> {
  final _formKey = GlobalKey<FormState>();
  final CourseService _courseService = CourseService();

  String _title = '';
  bool _isCompleted = false;
  int? _departmentId;
  List<int> _gainedSkills = [];
  List<int> _requiredSkills = [];
  List<int> _professors = [];

  Future<void> _submitCourse() async {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();

      final courseData = {
        "title": _title,
        "is_completed": _isCompleted,
        "department": _departmentId,
        "gainedSkills": _gainedSkills,
        "requiredSkills": _requiredSkills,
        "professors": _professors,
      };

      print("Submitting Course Data: $courseData"); // Debugging

      try {
        await _courseService.createCourse(courseData);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Course created successfully!')),
        );
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to create course: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Create Course')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              TextFormField(
                decoration: InputDecoration(labelText: 'Title'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter a title';
                  }
                  return null;
                },
                onSaved: (value) {
                  _title = value!;
                },
              ),
              SwitchListTile(
                title: Text('Is Completed'),
                value: _isCompleted,
                onChanged: (value) {
                  setState(() {
                    _isCompleted = value;
                  });
                },
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Department ID'),
                keyboardType: TextInputType.number,
                onSaved: (value) {
                  _departmentId = int.tryParse(value!);
                },
              ),
              TextFormField(
                decoration: InputDecoration(
                    labelText: 'Gained Skills (comma-separated IDs)'),
                onSaved: (value) {
                  _gainedSkills = value!
                      .split(',')
                      .map((e) => int.tryParse(e.trim()) ?? 0)
                      .toList();
                },
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Title'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter a title';
                  }
                  return null;
                },
                onSaved: (value) {
                  _title = value!;
                },
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Department ID'),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter a department ID';
                  }
                  if (int.tryParse(value) == null) {
                    return 'Department ID must be a number';
                  }
                  return null;
                },
                onSaved: (value) {
                  _departmentId = int.tryParse(value!);
                },
              ),
              TextFormField(
                decoration: InputDecoration(
                    labelText: 'Required Skills (comma-separated IDs)'),
                onSaved: (value) {
                  _requiredSkills = value!
                      .split(',')
                      .map((e) => int.tryParse(e.trim()) ?? 0)
                      .toList();
                },
              ),
              TextFormField(
                decoration: InputDecoration(
                    labelText: 'Professors (comma-separated IDs)'),
                onSaved: (value) {
                  _professors = value!
                      .split(',')
                      .map((e) => int.tryParse(e.trim()) ?? 0)
                      .toList();
                },
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: _submitCourse,
                child: Text('Create Course'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
