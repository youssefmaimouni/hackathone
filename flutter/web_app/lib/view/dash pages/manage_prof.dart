import 'package:flutter/material.dart';
import 'package:web_app/data/prof.dart';
import 'package:web_app/model/prof.dart';
import 'package:web_app/view/widget/update_prof.dart';

class ManageProf extends StatefulWidget {
  const ManageProf({super.key});

  @override
  State<ManageProf> createState() => _ManageProfState();
}

class _ManageProfState extends State<ManageProf> {
  late Future<List<Professor>> futureProfessors;

  get http => null;

  @override
  void initState() {
    super.initState();
    futureProfessors = fetchProfessors();
  }

  void _showUpdateDialog(Professor professor) {
    showDialog(
      context: context,
      builder: (context) {
        return UpdateProfessorPage(
          professorId: professor.id,
          firstName: professor.firstName,
          lastName: professor.lastName,
          email: professor.email,
        );
      },
    );
  }

// Show delete confirmation dialog
  void _showDeleteConfirmation(Professor professor) {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Confirm Deletion'),
          content: Text(
              'Are you sure you want to delete ${professor.firstName} ${professor.lastName}?'),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context); // Close the dialog
              },
              child: Text('Cancel'),
            ),
            TextButton(
              onPressed: () async {
                // Send DELETE request to remove the professor
                final response = await http.delete(
                  Uri.parse(
                      'http://127.0.0.1:5000/professors/${professor.id}'), // Replace with actual URL
                );

                if (response.statusCode == 200) {
                  setState(() {
                    futureProfessors =
                        fetchProfessors(); // Refresh the professor list after deletion
                  });
                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                      content: Text('Professor deleted successfully')));
                  Navigator.pop(context); // Close the dialog
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Failed to delete professor')));
                  Navigator.pop(context); // Close the dialog
                }
              },
              child: Text('Delete'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Professors')),
      body: FutureBuilder<List<Professor>>(
        future: futureProfessors,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No professors found.'));
          } else {
            return ListView.builder(
              itemCount: snapshot.data!.length,
              itemBuilder: (context, index) {
                final professor = snapshot.data![index];
                return ListTile(
                  title: Text('${professor.firstName} ${professor.lastName}'),
                  subtitle: Text(professor.email),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: Icon(Icons.edit),
                        onPressed: () {
                          _showUpdateDialog(
                              professor); // Show the update dialog when the button is pressed
                        },
                      ),
                      IconButton(
                        icon: Icon(Icons.delete),
                        onPressed: () {
                          _showDeleteConfirmation(
                              professor); // Show the delete confirmation dialog
                        },
                      ),
                    ],
                  ),
                );
              },
            );
          }
        },
      ),
    );
  }
}
