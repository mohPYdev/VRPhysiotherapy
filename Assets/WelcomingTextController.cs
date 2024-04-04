using UnityEngine;
using UnityEngine.UI;

public class WelcomingTextController : MonoBehaviour
{
    public GameObject welcomingText;


    public void ShowWelcomingText()
    {
        welcomingText.SetActive(true);
    }
}
