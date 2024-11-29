import 'package:flutter/material.dart';
import 'package:web_app/data/prof.dart';
import 'package:web_app/model/prof.dart';

class ListProf extends StatefulWidget {
  const ListProf({super.key});

  @override
  State<ListProf> createState() => _ListProfState();
}

class _ListProfState extends State<ListProf> {
  late Future<List<Professor>> futureProfessors;

  @override
  void initState() {
    super.initState();
    futureProfessors = fetchProfessors();
  }

  @override
  Widget build(BuildContext context) {
    Size mq = MediaQuery.of(context).size;
    return Container(
      padding: const EdgeInsets.all(10),
      child: Column(
        children: [
          Row(
            children: [
              Container(
                margin: const EdgeInsets.only(right: 10),
                decoration: const BoxDecoration(
                    color: Colors.blueAccent,
                    borderRadius: BorderRadius.all(Radius.circular(3))),
                width: mq.width * 0.04,
                child: const Padding(
                  padding: EdgeInsets.only(left: 12),
                  child: Text(
                    "N.",
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
              Container(
                margin: const EdgeInsets.only(right: 10),
                decoration: const BoxDecoration(
                    color: Colors.blueAccent,
                    borderRadius: BorderRadius.all(Radius.circular(3))),
                width: mq.width * 0.12,
                child: const Padding(
                  padding: EdgeInsets.only(left: 12),
                  child: Text(
                    "First Name",
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
              Container(
                margin: const EdgeInsets.only(right: 10),
                decoration: const BoxDecoration(
                    color: Colors.blueAccent,
                    borderRadius: BorderRadius.all(Radius.circular(3))),
                width: mq.width * 0.12,
                child: const Padding(
                  padding: EdgeInsets.only(left: 12),
                  child: Text(
                    "Last Name",
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
              Container(
                margin: const EdgeInsets.only(right: 10),
                decoration: const BoxDecoration(
                    color: Colors.blueAccent,
                    borderRadius: BorderRadius.all(Radius.circular(3))),
                width: mq.width * 0.2,
                child: const Padding(
                  padding: EdgeInsets.only(left: 12),
                  child: Text(
                    "Email",
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
              Container(
                margin: const EdgeInsets.only(right: 10),
                decoration: const BoxDecoration(
                    color: Colors.blueAccent,
                    borderRadius: BorderRadius.all(Radius.circular(3))),
                width: mq.width * 0.1,
                child: const Padding(
                    padding: EdgeInsets.only(left: 12),
                    child: Text(
                      "Hire Date",
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w700,
                        color: Colors.white,
                      ),
                    )),
              ),
              Container(
                decoration: const BoxDecoration(
                    color: Colors.blueAccent,
                    borderRadius: BorderRadius.all(Radius.circular(3))),
                width: mq.width * 0.1,
                child: const Padding(
                  padding: EdgeInsets.only(left: 12, right: 12),
                  child: Text(
                    "Manage",
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
            ],
          ),
          FutureBuilder<List<Professor>>(
            future: futureProfessors,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(child: CircularProgressIndicator());
              } else if (snapshot.hasError) {
                return SizedBox(
                  height: mq.height * 0.94,
                  width: mq.width * 0.74,
                  child: Center(
                      child: Text(
                    'Error: ${snapshot.error}',
                    style: const TextStyle(
                      color: Colors.black,
                    ),
                  )),
                );
              } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                return const Center(
                    child: Text(
                  'No professors found.',
                  style: TextStyle(
                    color: Colors.black,
                  ),
                ));
              } else {
                return SizedBox(
                  height: mq.height * 0.8,
                  width: mq.width * 0.74,
                  child: ListView.builder(
                    scrollDirection: Axis.vertical,
                    itemCount: snapshot.data!.length,
                    itemBuilder: (context, index) {
                      final professor = snapshot.data![index];
                      return ListTile(
                        title: Text(
                          '${professor.firstName} ${professor.lastName}',
                          style: const TextStyle(
                            color: Colors.black,
                          ),
                        ),
                        subtitle: Text(professor.email),
                        trailing: professor.isActive == true
                            ? const Icon(Icons.check_circle,
                                color: Colors.green)
                            : const Icon(Icons.cancel, color: Colors.red),
                      );
                    },
                  ),
                );
              }
            },
          ),
        ],
      ),
    );
  }
}
