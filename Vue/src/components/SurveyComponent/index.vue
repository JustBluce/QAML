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
                let formData = new FormData();
                formData.append("survey", sender.data)
                this.axios({
              url: "http://127.0.0.1:5000/users/survey",
              headers: {
                "content-Type": "application/json; charset=utf-8",
            },
              method: "POST",
              data: formData,
            }).then((response) => { 
                console.log(response)
            })
})
           
       

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
