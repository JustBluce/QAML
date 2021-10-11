<template>
    <survey :survey="survey" />
</template>

<script>
    
    
    import * as Survey from "survey-vue";
    

    
    import "survey-vue/modern.css";
    import "./index.css";

    Survey.StylesManager.applyTheme("modern");

    export default {
        name: "surveyjs-component",
        data() {
            
            
            

            

            const json = {
                "completedHtml": "<h3>Thank you for your feedback.</h3> <h5>Your thoughts and ideas will help us to create a great product!</h5>",
                "completedHtmlOnCondition": [
                {
                "expression": "{rating} > 8",
                "html": "<h3>Thank you for your feedback.</h3> <h5>We glad that you love our product. Your ideas and suggestions will help us to make our product even better!</h5>"
                },
                {
                    "expression": "{rating} < 7",
                    "html": "<h3>Thank you for your feedback.</h3> <h5> We are glad that you share with us your ideas.We highly value all suggestions from our customers. We do our best to improve the product and reach your expectation.</h5><br/>"
                }
                ],
                "pages": [
                {
                "name": "page1",
                "elements": [
                    {
                    "type": "rating",
                    "name": "rating",
                    "title": "On a scale of zero to ten, how likely are you to recommend our product to a friend or colleague?",
                    "isRequired": true,
                    "rateMin": 0,
                    "rateMax": 10,
                    "minRateDescription": "(Most unlikely)",
                    "maxRateDescription": "(Most likely)"
                    },
                    {
                    "type": "checkbox",
                    "name": "promoter_features",
                    "title": "What features do you value the most?",
                    "isRequired": true,
                    "validators": [
                    {
                    "type": "answercount",
                    "text": "Please select two features maximum.",
                    "maxCount": 2
                    }
                    ],
                    "hasOther": true,
                    "choices": [
                    "Performance",
                    "Stability",
                    "User Interface",
                    "Complete Functionality"
                    ],
                    "otherText": "Other feature:",
                    "colCount": 2
                    },
                    {
                    "type": "comment",
                    "name": "additional_comments",
                    "title": "What is the primary reason for your score?"
                    },
                    
                ]
                }
                ],
                "showQuestionNumbers": "off"
                }
                ;


            const survey = new Survey.Model(json);

           survey.onComplete.add(function (sender, options) {
                //Show message about "Saving..." the results
                options.showDataSaving();//you may pass a text parameter to show your own text 
                var xhr = new XMLHttpRequest();
                const formData = new FormData()

                formData.append("survey", sender.data)
            
                xhr.open("POST", "http://127.0.0.1:5000/users/survey");
                xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");
                xhr.onload = xhr.onerror = function () {
                    if (xhr.status == 200) {
                        options.showDataSavingSuccess(); // you may pass a text parameter to show your own text
                        // Or you may clear all messages:
                        // options.showDataSavingClear();
                    } else {
                        //Error
                        options.showDataSavingError(); // you may pass a text parameter to show your own text
                    }
                };
                //xhr.send(formData)
                
              
                xhr.send(JSON.stringify(sender.data));
});
           
       

            return {
                survey: survey
            };
            
        }  

    };

    // For Future Reference
    // https://surveyjs.io/Documentation/Library 


</script>

<style scoped>
</style>
