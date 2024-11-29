import 'package:flutter/material.dart';
import 'package:web_app/data/course_data.dart';

class ListCourse extends StatelessWidget {
  final CourseService courseService = CourseService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Courses")),
      body: FutureBuilder<List<dynamic>>(
        future: courseService.fetchCourses(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No courses available'));
          } else {
            final courses = snapshot.data!;
            return ListView.builder(
              itemCount: courses.length,
              itemBuilder: (context, index) {
                final course = courses[index];
                return ListTile(
                  title: Text(course['title']),
                  subtitle: Text(
                      "Department: ${course['department'] ?? 'Unknown'}"),
                );
              },
            );
          }
        },
      ),
    );
  }
}
