// Future<void> createCourse(Map<String, dynamic> courseData) async {
//   try {
//     final response = await http.post(
//       Uri.parse('$baseUrl/courses'),
//       headers: {'Content-Type': 'application/json'},
//       body: json.encode(courseData),
//     );

//     if (response.statusCode != 201) {
//       throw Exception('Failed to create course');
//     }
//   } catch (e) {
//     throw Exception('Error: $e');
//   }
// }
