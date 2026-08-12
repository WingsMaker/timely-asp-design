# EC2 instance for the secure agent. Fill AMI and subnet/etc before applying.
resource "aws_instance" "agent" {
  ami           = "ami-REPLACE_ME"
  instance_type = var.ec2_instance_type
  iam_instance_profile = aws_iam_instance_profile.ec2_agent_profile.name

  tags = {
    Name = "timely-asp-agent"
  }

  # user_data can be used to bootstrap the agent (install python, pip, pull repo, etc.)
  user_data = file("../../infra/terraform/user_data/agent_bootstrap.sh")
}

resource "aws_iam_instance_profile" "ec2_agent_profile" {
  name = "timely_asp_ec2_agent_profile"
  role = aws_iam_role.ec2_agent_role.name
}
