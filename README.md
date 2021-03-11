# albuminator

[![Demo](https://res.cloudinary.com/marcomontalbano/image/upload/v1615360313/video_to_markdown/images/youtube--Ox2wN14sImY-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=Ox2wN14sImY&ab_channel=NithishBolleddula "Demo")


# Deploying the application on EC2

1. Start ec2-instance and with port 80 and 8000 added in the inbound rules.

In ec2-instance terminal:

    docker pull nithishreddy/albuminator:latest
    docker run -p 8000:8000 nithishreddy/albuminator:latest
    

From client-browser
open

    http://<public-ip-of-ec2-instance>:8000



