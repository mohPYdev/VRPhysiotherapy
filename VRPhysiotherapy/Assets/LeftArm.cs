using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;


public class LeftArm : MonoBehaviour
{
    public void GoToNextScene()
    {
        SceneManager.LoadSceneAsync(3);
    }

    public void GoToBackScene()
    {
        SceneManager.LoadSceneAsync(1);
    }
}
