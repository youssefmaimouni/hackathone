import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:web_app/model/prof.dart';

Future<List<Professor>> fetchProfessors() async {
  final response = await http.get(
      Uri.parse('http://127.0.0.1:5000/professors')); // Your Flask server URL

  if (response.statusCode == 200) {
    final List<dynamic> data =
        jsonDecode(response.body); // Parse the JSON response
    return data.map((json) => Professor.fromJson(json)).toList();
  } else {
    throw Exception('Failed to load professors'); // Handle errors
  }
}
