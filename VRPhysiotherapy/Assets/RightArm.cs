using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class RightArm : MonoBehaviour
{
    public void GoToNextScene()
    {
        SceneManager.LoadSceneAsync(4);
    }

    public void GoToBackScene()
    {
        SceneManager.LoadSceneAsync(2);
    }
}
