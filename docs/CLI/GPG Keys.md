# GPG Keys

1. Download and install [the GPG Privacy Guard](https://www.gnupg.org) for your operating system

Linux
```shell
# Debian and Ubuntu
sudo apt install gnupg
```

```shell
# Arch and Manjaro
sudo pacman -S gnupg
```

2. Open the terminal and Generate a GPG key pair

```shell
gpg --full-generate-key
```

3. At the prompt, specify the kind of key you want, or press `Enter` to accept the default

4. At the prompt, specify the key size you want, or press `Enter` to accept the default. Your key must be at least `4096` bits

5. Enter the length of time the key should be valid. Press `Enter` to specify the default selection, indicating that the key doesn't expire. Unless you require an expiration date, we recommend accepting this default

6. Verify that your selections are correct

7. Enter your user ID information and type a secure passphrase.

**Note:** 
	When asked to enter your email address, ensure that you enter the verified email address for your GitHub account. To keep your email address private, use your GitHub-provided `no-reply` email address. For more information, see "[Verifying your email address](https://docs.github.com/en/get-started/signing-up-for-github/verifying-your-email-address)" and "[Setting your commit email address](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address)."
  
8. Use the `gpg --list-secret-keys --keyid-format=long` command to list the long form of the GPG keys for which you have both a public and private key. A private key is required for signing commits or tags.

```shell
gpg --list-secret-keys --keyid-format=long
```

9. Paste the text below, substituting in the GPG key ID you'd like to use

``` shell
$ gpg --armor --export 3AA5C34371567BD2
# Prints the GPG key ID, in ASCII armor format
```

10. Copy your GPG key, beginning with `-----BEGIN PGP PUBLIC KEY BLOCK-----` and ending with `-----END PGP PUBLIC KEY BLOCK-----`.

11. Add that to your `~/.bashrc` or `˜/.bash_profile` the line `export GPG_TTY=$(tty)`

12. [Add the GPG key to your GitHub account](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account).