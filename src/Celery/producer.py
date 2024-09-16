from ml_app import predict

def main():
    while True:
        msg = input("Enter a message: ")
        if msg == "exit":
            break

        # Call Celery task
        payload = {"message": msg}
        result = predict.delay(payload)
    
if __name__ == "__main__":
    main()
