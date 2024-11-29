import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class Admin extends StatefulWidget {
  @override
  _AdminState createState() => _AdminState();
}

class _AdminState extends State<Admin> {
  String email = '';
  String firstName = '';
  String lastName = '';

  // Function to fetch profile data from the backend
  Future<void> fetchProfile() async {
    final response = await http.get(Uri.parse('http://localhost:5000/profile'));

    if (response.statusCode == 200) {
      final Map<String, dynamic> data = json.decode(response.body);
      setState(() {
        email = data['email'];
        firstName = data['first_name'];
        lastName = data['last_name'];
      });
    } else {
      throw Exception('Failed to load profile data');
    }
  }

  @override
  void initState() {
    super.initState();
    fetchProfile();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          'Profile',
          style: TextStyle(color: Colors.white),
        ),
        backgroundColor: Colors.black.withOpacity(0.8),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SizedBox(
          height: double.infinity,
          width: double.infinity,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              // Profile Picture

              SizedBox(height: 20),
              Icon(
                Icons.supervised_user_circle,
                size: 40,
                color: Colors.blue,
              ),
              SizedBox(height: 8),

              Text(
                '$firstName $lastName',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.blueAccent,
                ),
              ),
              SizedBox(height: 10),

              // Email Section
              Text(
                email,
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.grey[600],
                ),
              ),
              SizedBox(height: 20),

              // Edit Button
            ],
          ),
        ),
      ),
    );
  }
}
