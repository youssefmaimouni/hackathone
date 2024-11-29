import 'package:flutter/material.dart';
import 'package:web_app/view/widget/login_screen.dart';

class Login extends StatefulWidget {
  const Login({super.key});

  @override
  State<Login> createState() => _LoginState();
}

class _LoginState extends State<Login> {
  @override
  Widget build(BuildContext context) {
    Size mq = MediaQuery.of(context).size;
    return Scaffold(
      body: Stack(
        alignment: AlignmentDirectional.center,
        children: [
          Container(
            height: double.infinity,
            width: double.infinity,
            decoration: const BoxDecoration(
                image: DecorationImage(
                    image: AssetImage(
                        "assets/marita-kavelashvili-ugnrXk1129g-unsplash.jpg"),
                    fit: BoxFit.fill)),
          ),
          Container(
            height: double.infinity,
            width: double.infinity,
            decoration: BoxDecoration(color: Colors.black.withOpacity(0.4)),
          ),
          Container(
            height: mq.height * 0.9,
            width: mq.width * 0.7,
            decoration: const BoxDecoration(
              borderRadius: BorderRadius.all(Radius.circular(16)),
              color: Colors.white,
            ),
            child: Row(
              children: [
                Expanded(
                    flex: 3,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 20),
                      alignment: AlignmentDirectional.center,
                      margin: const EdgeInsets.all(10),
                      decoration: const BoxDecoration(
                          borderRadius: BorderRadius.all(Radius.circular(10))),
                      child: const LoginScreen(),
                    )),
                Expanded(
                    flex: 4,
                    child: Container(
                      margin: const EdgeInsets.all(14),
                      decoration: const BoxDecoration(
                          borderRadius: BorderRadius.all(Radius.circular(10)),
                          image: DecorationImage(
                              image: AssetImage(
                                  "assets/marita-kavelashvili-ugnrXk1129g-unsplash.jpg"),
                              fit: BoxFit.cover)),
                    )),
              ],
            ),
          )
        ],
      ),
    );
  }
}
