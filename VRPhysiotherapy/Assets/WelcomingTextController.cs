using UnityEngine;
using UnityEngine.UI;

public class WelcomingTextController : MonoBehaviour
{
    public GameObject welcomingText;
    public GameObject left_avatar;
    public GameObject right_avatar;
    public GameObject camera;
    public GameObject teleport_location;
    public void ShowWelcomingText()
    {
        welcomingText.SetActive(true);
    }

    public void GoToNextStepLeft()
    {
        //SceneManager.LoadSceneAsync(1);
        gameObject.SetActive(false);
        left_avatar.gameObject.SetActive(true);
    }

    public void GoToNextStepRight()
    {
        //SceneManager.LoadSceneAsync(1);
        left_avatar.gameObject.SetActive(false);
        right_avatar.gameObject.SetActive(true);
    }
    public void GoToBackStepRight()
    {
        left_avatar.gameObject.SetActive(true);
        right_avatar.gameObject.SetActive(false);
    }
    public void GoToStartPoint()
    {
        camera.transform.position = teleport_location.transform.position;
    }
}
