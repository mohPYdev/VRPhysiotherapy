using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using System.IO;
using TMPro;
public class MainMenu : MonoBehaviour
{
    public TextMeshProUGUI history_text;
    public string filePath = "Assets/HistoryFiles/history_text.txt";

    public void PlayGame()
    {
        SceneManager.LoadSceneAsync(1);
        AudioManager.instance.PlaySFX("Play_Game");
    }
    public void ExitButton()
    {
        AudioManager.instance.PlaySFX("Click_Button");
        print("Exit");
        Application.Quit();

    }
    public void OptionButton()
    {
        AudioManager.instance.PlaySFX("Click_Button");
    }
    public void Exit_OptionPanel()
    {
        AudioManager.instance.PlaySFX("Click_Button");
    }
    public void TrainingOptionButton()
    {
        AudioManager.instance.PlaySFX("Click_Button");
    }
    public void HistoryButton()
    {
        AudioManager.instance.PlaySFX("Click_Button");
        //string filePath = Application.persistentDataPath + "/savedata.txt";

        if (File.Exists(filePath))
        {
            // Read data from file
            // Read the text from the file
            string[] lines = File.ReadAllLines(filePath);
            string textToShow = string.Join("\n", lines);
            print(textToShow);
            history_text.text = textToShow;
        }
        else
        {
            Debug.Log("No saved data found.");
        }

    }
    public void HelpBoutton()
    {
        AudioManager.instance.PlaySFX("Click_Button");
    }
}
