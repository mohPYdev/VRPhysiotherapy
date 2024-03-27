using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
public class MainMenu : MonoBehaviour
{
    public void PlayGame()
    {
        SceneManager.LoadSceneAsync(1);
<<<<<<< Updated upstream
    }
    public void ExitButton()
    {
=======
        AudioManager.instance.PlaySFX("Play_Game");
    }
    public void ExitButton()
    {
        AudioManager.instance.PlaySFX("Click_Button");
>>>>>>> Stashed changes
        print("Exit");
        Application.Quit();

    }
<<<<<<< Updated upstream
=======
    public void OptionButton()
    {
        AudioManager.instance.PlaySFX("Click_Button");
    }
    public void Exit_OptionPanel()
    {
        AudioManager.instance.PlaySFX("Click_Button");
    }
    
>>>>>>> Stashed changes
}
