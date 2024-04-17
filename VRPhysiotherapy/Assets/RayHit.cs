using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;
using UnityEngine.SceneManagement;


public class RayHit : MonoBehaviour
{
    public GameObject textObject;
    public GameObject menu;
    public void active_text()
    {
        if (! menu.activeSelf)
        {
            textObject.SetActive(true);
        }
    }
    public void deactive_text()
    {
        textObject.SetActive(false);
    }
    public void show_menu()
    {
        if (! menu.activeSelf)
        {         
            menu.SetActive(true);
            textObject.SetActive(false);
            Time.timeScale = 0.0f;
        }   
    }
    public void disappear_menu()
    {
        
        menu.SetActive(false);
        Time.timeScale = 1.0f;
    }
    public void go_main_menu()
    {
        SceneManager.LoadScene(1);
    }
    public void go_training()
    {
        SceneManager.LoadScene(2);
    }
}

