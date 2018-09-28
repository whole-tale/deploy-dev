Setting up local testing instance of Girder
===========================================

Requirements:

 * docker >= 18.04
 * GitHub app OAuth credentials with callback set to `http://girder.vcap.me/api/v1/oauth/github/callback`.
   Export them using env variables:
   * GITHUB_CLIENT_ID
   * GITHUB_CLIENT_SECRET

Clone this repository:

```
git clone https://github.com/whole-tale/girder_deploy
```

Go to `wt_dev` directory and run:

```
cd girder_deploy/wt_dev
make dev
```

To shutdown

```
make clean
```
