import 'package:flutter/material.dart';
import 'package:web_app/model/recomandation.dart';

class Recommendations extends StatefulWidget {
  const Recommendations({super.key});

  @override
  State<Recommendations> createState() => _RecommendationsState();
}

class _RecommendationsState extends State<Recommendations> {
  TextEditingController _searchController = TextEditingController();

  List<Course> courses = [
    Course(title: 'Data Science', relatedCourses: ['AI', 'Machine Learning']),
    Course(
        title: 'Graphic Design',
        relatedCourses: ['Video Editing', 'OS Basics']),
    Course(
        title: 'Web Development',
        relatedCourses: ['JavaScript', 'Front-End Frameworks']),
    Course(title: 'AI', relatedCourses: ['Data Science', 'Deep Learning']),
    Course(
        title: 'Video Editing',
        relatedCourses: ['Graphic Design', 'OS Basics']),
  ];

  List<Course> filteredCourses = [];
  List<String> recommendedCourses = [];
  void _filterCourses(String query) {
    setState(() {
      filteredCourses = courses
          .where((course) =>
              course.title.toLowerCase().contains(query.toLowerCase()))
          .toList();

      // If a course is selected, show related courses
      if (query.isNotEmpty) {
        recommendedCourses = courses
            .where((course) =>
                course.title.toLowerCase().contains(query.toLowerCase()))
            .expand((course) => course.relatedCourses)
            .toSet()
            .toList();
      } else {
        recommendedCourses = [];
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Course Recommendations'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            // Search Bar
            TextField(
              controller: _searchController,
              decoration: InputDecoration(
                labelText: 'Search Courses',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.search),
              ),
              onChanged: _filterCourses,
            ),
            SizedBox(height: 16.0),
            // List of filtered courses
            Expanded(
              child: ListView.builder(
                itemCount: filteredCourses.length,
                itemBuilder: (context, index) {
                  final course = filteredCourses[index];
                  return ListTile(
                    title: Text(course.title),
                    onTap: () {
                      // Show related courses when a course is selected
                      setState(() {
                        recommendedCourses = course.relatedCourses;
                      });
                    },
                  );
                },
              ),
            ),
            // Display recommended courses
            if (recommendedCourses.isNotEmpty)
              Padding(
                padding: EdgeInsets.symmetric(vertical: 16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Recommended Courses:',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    ...recommendedCourses.map((course) => ListTile(
                          title: Text(course),
                        )),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }
}
