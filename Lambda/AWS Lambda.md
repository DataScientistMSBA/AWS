### 1. In AWS, go to the Lambda module anc click on **Create Function**.
### 2. **Author from scratch**, give it a **Function name** and select a Python based **Runtime**.
### 3. Open up the **Change default execution role** and select **Use an existing role**.
### 4. If you have no existing roles to select from then you will need to create one. To do this, do the following:
- a. Go to **OneCloud** and select the **Accounts** tab.
- b. Scroll down and select **Roles**.
- c. Select **Create custom role**.
- d. Enter a **Role Name** and select what sort of **Purpose** is appropriate. If creating a role for an AWS service (like Lambda), select **Service**.
- e. Search for the appropriate **Service Namespace** if a **Service** **Purpuse** is selected.
- f. Press **Create Role**.
- g. Exit **OneCloud** and go to the associated **AWS Console** and go to the **IAM** module.
- h. Select **Roles** on the left panel and search for associated role name from step d.
- j.  Under **Permissions policies**, select **Add permissions** and add the appropriate permissions based off its use case.
### 5. Select the appropriate **Existing role** and click **Create function**.


