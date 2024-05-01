using WebSocketSharp;
using UnityEngine;

public class SocketClient : MonoBehaviour
{
    WebSocket ws;
    int a = 0;
    void Start()
    {
        ws = new WebSocket("ws://127.0.0.1:8080");
        ws.OnMessage += (sender, e) =>
        {
            Debug.Log("Mesasge was received from " + ((WebSocket)sender).Url + ", Data : " + e.Data);
        };
        ws.Connect();
    }

    void Update()
    {
        a++;
        if (ws == null)
        {
            return;
        }

        if (Input.GetKeyDown(KeyCode.Space))
        {
            // Do something when space is pressed
            Debug.Log("Space key pressed");
            start_movement();
        }

        // Check if the enter key is pressed
        if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.KeypadEnter))
        {
            // Do something when enter is pressed
            Debug.Log("Enter key pressed");
            end_movement();
        }

    }

    public void start_movement()
    {
        ws.Send("Start");
    }

    public void end_movement()
    {
        ws.Send("End");
    }
}