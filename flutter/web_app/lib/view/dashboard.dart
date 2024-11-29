import 'package:flutter/material.dart';
import 'package:sidebar_with_animation/animated_side_bar.dart';
import 'package:web_app/view/dash%20pages/admin.dart';
import 'package:web_app/view/dash%20pages/create_course.dart';
import 'package:web_app/view/dash%20pages/create_prof.dart';
import 'package:web_app/view/dash%20pages/home.dart';
import 'package:web_app/view/dash%20pages/list_course.dart';
import 'package:web_app/view/dash%20pages/list_prof.dart';
import 'package:web_app/view/dash%20pages/manage_course.dart';
import 'package:web_app/view/dash%20pages/manage_prof.dart';
import 'package:web_app/view/dash%20pages/recommendations.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  List<Widget> screens = [
    Home(),
    const ListProf(),
    const CreateProf(),
    ListCourse(),
    const ManageProf(),
    CreateCourse(),
    const Recommendations(),
    Admin()
  ];
  List<SideBarItem> sidebarItems = [
    SideBarItem(
      iconSelected: Icons.home_filled,
      text: "Home",
    ),
    SideBarItem(
      iconSelected: Icons.school_rounded,
      text: "List professors",
    ),
    SideBarItem(
      iconSelected: Icons.add_box_rounded,
      text: "Create professors",
    ),
    SideBarItem(
      iconSelected: Icons.golf_course,
      text: "List courses",
    ),
    SideBarItem(
      iconSelected: Icons.add_box_rounded,
      text: "Manage Professors",
    ),
    SideBarItem(
      iconSelected: Icons.edit,
      text: "Manage courses",
    ),
    SideBarItem(
      iconSelected: Icons.recommend,
      text: "Recommendations",
    ),
    SideBarItem(
      iconSelected: Icons.admin_panel_settings_rounded,
      text: "Admin Page",
    ),
  ];
  int index = 0;
  @override
  Widget build(BuildContext context) {
    Size mq = MediaQuery.of(context).size;
    return Scaffold(
      body: Row(
        children: [
          SideBarAnimated(
            // sideBarColor: ct.primary,
            // hoverColor: ct.onSurface.withOpacity(0.1),
            // splashColor: ct.onSurface.withOpacity(0.2),
            // unSelectedTextColor: ct.background,
            // unselectedIconColor: ct.background,
            mainLogoImage: "assets/img2.png",
            sidebarItems: sidebarItems,
            widthSwitch: mq.width * 0.4,
            onTap: (value) {
              setState(() {
                index = value;
              });
            },
          ),
          Container(
            height: mq.height * 0.94,
            width: mq.width * 0.74,
            margin: EdgeInsets.only(left: mq.width * 0.015),
            child: screens[index],
          ),
        ],
      ),
    );
  }
}
