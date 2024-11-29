import 'package:flutter/material.dart';
import 'package:web_app/view/login.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    Size mq = MediaQuery.of(context).size;
    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            Stack(
              children: [
                Container(
                  height: mq.height,
                  width: mq.width,
                  decoration: const BoxDecoration(
                      image: DecorationImage(
                          image: AssetImage("assets/img.jpg"),
                          fit: BoxFit.cover)),
                ),
                Container(
                  height: mq.height,
                  width: mq.width,
                  color: Colors.black.withOpacity(0.5),
                  child: Column(
                    children: [
                      Padding(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 66, vertical: 16),
                        child: Row(
                          children: [
                            const Text(
                              'Dataverse & Open Source',
                              style: TextStyle(
                                  fontSize: 18,
                                  color: Colors.white,
                                  fontWeight: FontWeight.w700),
                            ),
                            const Expanded(child: SizedBox(width: 10)),
                            ElevatedButton(
                              style: ButtonStyle(
                                  backgroundColor:
                                      WidgetStateProperty.all<Color>(
                                          Colors.deepPurple),
                                  shape: WidgetStateProperty.all<
                                          RoundedRectangleBorder>(
                                      RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(4.0),
                                  ))),
                              onPressed: () {
                                Navigator.pushReplacement(
                                  context,
                                  MaterialPageRoute(
                                      builder: (context) => const Login()),
                                );
                              },
                              child: const Padding(
                                padding: EdgeInsets.symmetric(
                                    vertical: 6.0, horizontal: 16),
                                child: Text(
                                  'Login now',
                                  style: TextStyle(
                                      fontSize: 12,
                                      color: Colors.white,
                                      fontWeight: FontWeight.w700),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      Row(
                        children: [
                          Expanded(
                              child: Container(
                            padding: const EdgeInsets.only(left: 66, top: 124),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Empowering learning with Recommendation',
                                  style: TextStyle(
                                      fontSize: 44,
                                      color: Colors.white,
                                      fontWeight: FontWeight.w700),
                                ),
                                const SizedBox(height: 16),
                                const Text(
                                  'Get the best recommendation for your next course \nin your system',
                                  style: TextStyle(
                                      fontSize: 16,
                                      color: Colors.white,
                                      fontWeight: FontWeight.w500),
                                  textAlign: TextAlign.left,
                                ),
                                const SizedBox(height: 16),
                                ElevatedButton(
                                  style: ButtonStyle(
                                      backgroundColor:
                                          WidgetStateProperty.all<Color>(
                                              Colors.deepPurple),
                                      shape: WidgetStateProperty.all<
                                              RoundedRectangleBorder>(
                                          RoundedRectangleBorder(
                                        borderRadius:
                                            BorderRadius.circular(4.0),
                                      ))),
                                  onPressed: () {
                                    Navigator.pushReplacement(
                                      context,
                                      MaterialPageRoute(
                                          builder: (context) => const Login()),
                                    );
                                  },
                                  child: const Padding(
                                    padding: EdgeInsets.symmetric(
                                        vertical: 10.0, horizontal: 14),
                                    child: Text(
                                      'Login now',
                                      style: TextStyle(
                                          fontSize: 16,
                                          color: Colors.white,
                                          fontWeight: FontWeight.w700),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          )),
                          const Expanded(child: SizedBox())
                        ],
                      ),
                      Padding(
                        padding:
                            const EdgeInsets.only(top: 40, left: 66, right: 66),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Container(
                              height: 90,
                              width: 300,
                              decoration: BoxDecoration(
                                  color: Colors.blueAccent.withOpacity(0.5),
                                  borderRadius: const BorderRadius.all(
                                      Radius.circular(8))),
                              child: const Padding(
                                padding: EdgeInsets.symmetric(horizontal: 8.0),
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    Icon(
                                      Icons.table_chart_outlined,
                                      size: 34,
                                      color: Colors.white,
                                    ),
                                    SizedBox(width: 8),
                                    Text(
                                      'Recommendation system',
                                      style: TextStyle(
                                          fontSize: 16,
                                          color: Colors.white,
                                          fontWeight: FontWeight.w700),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                            Container(
                              height: 90,
                              width: 300,
                              decoration: BoxDecoration(
                                  color: Colors.orangeAccent.withOpacity(0.5),
                                  borderRadius: const BorderRadius.all(
                                      Radius.circular(8))),
                              child: const Padding(
                                padding: EdgeInsets.symmetric(horizontal: 8.0),
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    Icon(
                                      Icons.data_usage_rounded,
                                      size: 34,
                                      color: Colors.white,
                                    ),
                                    SizedBox(width: 8),
                                    Text(
                                      'Data Visualization',
                                      style: TextStyle(
                                          fontSize: 16,
                                          color: Colors.white,
                                          fontWeight: FontWeight.w700),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                            Container(
                              height: 90,
                              width: 300,
                              decoration: BoxDecoration(
                                  color: Colors.redAccent.withOpacity(0.5),
                                  borderRadius: const BorderRadius.all(
                                      Radius.circular(8))),
                              child: const Padding(
                                padding: EdgeInsets.symmetric(horizontal: 8.0),
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    Icon(
                                      Icons.golf_course_outlined,
                                      size: 34,
                                      color: Colors.white,
                                    ),
                                    SizedBox(width: 8),
                                    Text(
                                      'Management of courses',
                                      style: TextStyle(
                                          fontSize: 16,
                                          color: Colors.white,
                                          fontWeight: FontWeight.w700),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                            Container(
                              height: 90,
                              width: 300,
                              decoration: BoxDecoration(
                                  color: Colors.pinkAccent.withOpacity(0.5),
                                  borderRadius: const BorderRadius.all(
                                      Radius.circular(8))),
                              child: const Padding(
                                padding: EdgeInsets.symmetric(horizontal: 8.0),
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    Icon(
                                      Icons.school,
                                      size: 34,
                                      color: Colors.white,
                                    ),
                                    SizedBox(width: 8),
                                    Text(
                                      'Management of professors',
                                      style: TextStyle(
                                          fontSize: 16,
                                          color: Colors.white,
                                          fontWeight: FontWeight.w700),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ],
                        ),
                      )
                    ],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
