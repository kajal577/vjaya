from robot_control import RobotControl

robot = RobotControl()

if robot.connect():

    print("\nAI VISION ROBOT - BLUETOOTH TEST")
    print("F = Forward")
    print("B = Backward")
    print("L = Left")
    print("R = Right")
    print("S = Stop")
    print("Q = Quit")

    try:
        while True:
            command = input("\nEnter command: ").upper()

            if command == "F":
                robot.forward()
            elif command == "B":
                robot.backward()
            elif command == "L":
                robot.left()
            elif command == "R":
                robot.right()
            elif command == "S":
                robot.stop()
            elif command == "Q":
                break
            else:
                print("Invalid command")

    finally:
        robot.close()