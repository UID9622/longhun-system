# 如何在 Proton Mail 中使用自定义域名 | Proton

> Notion URL: https://app.notion.com/p/Proton-Mail-Proton-26a7125a9c9f81b68a8fe442cf53a3e4
> Created: 2025-09-10T21:09:00.000Z
> Last edited: 2025-09-10T21:09:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
Once you have a custom domain and a Proton Mail subscription, the next steps are to connect your custom domain to your Proton Mail account and add users and email addresses to your account. Below we provide instructions to complete each of these steps.
Note: If your domain’s nameservers are set to a service other than your domain registrar’s, you’ll need to update the DNS records through that service’s console (not through your registrar’s console).
1. Log in to your DNS console (located on the platform where you purchased the custom domain).
Note: If you don’t know how to access your DNS console or update DNS records, you can contact your domain name registrar to help you.2. Open another browser tab. Log in to the Proton Mail Domain names settings page at https://account.proton.me/mail/domain-names and click Add domain or Review.
3. Copy the DNS values (Type, Host name, Value/Data/Points to) from each tab and paste them into the correct fields in your DNS console as in the example below.
Note: You may need to follow the instructions from your domain name provider to create and update DNS records.
Here’s an example:
In the Proton tab Verify, the record Type is TXT, the Host name is @, and the DNS Value is protonmail-verification=xxx.
This means you must create a new DNS record in your DNS console. Select the record type TXT. Enter the character @ in the host name field and paste the value protonmail-verification=xxx into the value field.
- If your DNS console doesn’t accept @ as the host name, you can try to leave the host name field empty. Some providers might require entering the full domain name instead of “@”, or leaving the field empty.
Please note that domain providers sometimes have different or additional options. Here are some helpful tips:
- If the TTL field is available in your DNS console, you can set the value to 300 (it means the old DNS settings will be updated every five minutes).
- If your DNS console doesn’t accept the host name @, you can leave the host name field empty.
- If your DNS console doesn’t allow CNAME values to end with a dot, you can remove the last dot in the CNAME values.
4. Things you should be aware of when setting the email authentication (SPF/DKIM/DMARC) records:
- Major email services (such as Gmail) may reject or filter your emails to spam if SPF/DKIM/DMARC are missing or not set up properly.
- SPF allows Proton’s IPs to send emails for your domain. Make sure you have only one SPF record.
- DKIM allows Proton to cryptographically sign your emails. Make sure you add all three DKIM records.
- DMARC combines SPF and DKIM authentication results to prevent spoofing of your domain. We recommend using “p=quarantine” policy for most domains.
- You can learn more about how to set up SPF, DKIM, and DMARC in this article about anti-spoofing for custom domains.
5. Save the changes in your DNS console.
6. Proton Mail will automatically check to see if you have added the required records. This can take a few minutes or a few hours, depending on your previous TTL settings. A green check mark will appear on the Proton Mail Domain name settings page once each record has been verified.
Note: Even if all steps have a green check mark, a few platforms might still keep a record of your old settings for 1-3 days. If emails are still being delivered to your old mail server, check again later.
In the last step of the setup process, you can create new users for your custom domain or new addresses for existing users.
1. Click the Add user or Add address button to navigate to the Users and addresses settings page. You can also access that page by following this link: https://account.proton.me/mail/users-addresses
2. Click Add user to create a new user account for your custom domain. Or click Add address to create one or more new email addresses for an existing user.
3. Fill in the following details and click Save to create a new user account:
- Name
- Email address
- Password and confirm password
- Key strength (the default option is best for most people, but you may choose Compatibility if you’ve encountered a compatibility issue for PGP encrypted emails)
- Account storage
4. Congratulations! You’ve set up your custom domain in Proton Mail. It’s a good idea to double check your settings by going to the Domain names settings page and clicking Review to make sure all your DNS records have been verified.
## How to set up an organization in Proton Mail
Step 1: Set up your custom domain(s) (you are here)
Step 2: Create your organization
Step 3: Add new users to your organization
