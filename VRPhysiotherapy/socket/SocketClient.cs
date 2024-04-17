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
        if(ws == null)
        {
            return;
        }

        if (a == 100)
        {
            a = 0;
            ws.Send("Hello");
        }    
    }
}