docker run --name predict  -d -p 8000:8000  forcast

ssh  -l root -f -N -T -L 8088:localhost:8088 110.41.157.85

ssh  -l root -f -N -T -L 80:localhost:80 110.41.157.85


ssh  -l root -f -N -T -L 3307:192.168.0.167:3306 110.41.157.85
