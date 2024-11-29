class AdminProfile {
  final String firstName;
  final String lastName;
  final String email;

  AdminProfile({
    required this.firstName,
    required this.lastName,
    required this.email,
  });

  factory AdminProfile.fromJson(Map<String, dynamic> json) {
    return AdminProfile(
      firstName: json['first_name'],
      lastName: json['last_name'],
      email: json['email'],
    );
  }
}
