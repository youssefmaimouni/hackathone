import 'package:flutter/material.dart';

class Home extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: AppBar(title: Text('Display Statistics')),
        body: SingleChildScrollView(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // Image s1
              Image.asset(
                  'assets/s1.jpeg'), // Update with the path of your image
              // Image s2
              Image.asset(
                  'assets/s2.jpeg'), // Update with the path of your image
              // Image s3
              Image.asset(
                  'assets/s3.jpeg'), // Update with the path of your image
              // Image s4
              Image.asset(
                  'assets/s4.jpeg'), // Update with the path of your image
            ],
          ),
        ),
      ),
    );
  }
}
