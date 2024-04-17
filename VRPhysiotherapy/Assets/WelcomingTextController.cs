using UnityEngine;
using UnityEngine.UI;

public class WelcomingTextController : MonoBehaviour
{
    public GameObject welcomingText;
    public GameObject left_avatar;

    public void ShowWelcomingText()
    {
        welcomingText.SetActive(true);
    }

    public void GoToNextScene()
    {
        //SceneManager.LoadSceneAsync(1);
        gameObject.SetActive(false);
        left_avatar.gameObject.SetActive(true);
    }
}
