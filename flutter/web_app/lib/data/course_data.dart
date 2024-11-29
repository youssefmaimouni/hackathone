import 'dart:convert';
import 'package:http/http.dart' as http;

class CourseService {
  final String baseUrl =
      "http://localhost:5000"; // Replace with your backend URL

  Future<List<dynamic>> fetchCourses() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/courses'));

      if (response.statusCode == 200) {
        // Decode the JSON response into a list of courses
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load courses');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  Future<void> createCourse(Map<String, dynamic> courseData) async {
    print("Sending Data: $courseData");
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/courses'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(courseData),
      );
      print("Response Status: ${response.statusCode}");
      print("Response Body: ${response.body}");

      if (response.statusCode != 201) {
        throw Exception('Failed to create course: ${response.body}');
      }
    } catch (e) {
      print("Error: $e");
      throw Exception('Error: $e');
    }
  }
}
