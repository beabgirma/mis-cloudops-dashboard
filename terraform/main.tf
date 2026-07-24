terraform{
    required_providers{
        aws={
            source="hashicorp/aws"
            version = "~> 5.0"
        }
    }
}
provider "aws"{
    region ="us-east-1"

}
resource "aws_instance" "app_server" {
  ami           = "ami-0e2c8caa4b6378d8c" 
  instance_type = "t3.micro" # Updated to be compatible with your Free Tier settings
  tags = {
    Name = "MIS-Cloud_Dashboard"
  }
}