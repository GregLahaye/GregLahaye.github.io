# Adding Tailwind to a .NET 5 Web App

_This tutorial will demonstrate how to set up Tailwind CSS in a .NET Web App_

---

If you don't already have npm set up, run `npm init -y` in your project directory

---

Let's start by installing the required npm packages:

`npm i -D tailwindcss@latest postcss@latest postcss-cli@latest autoprefixer@latest`

---

Now we need to set up our postcss config, add following file to your project:

**postcss.config.js**
```
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  }
}
```

---

Next, we'll set up the Tailwind config with the following command:

`npx tailwind init`

This should create a tailwind.config.js file, we need to update this file to declare the files we want postcss to check when purging unused classes:

**tailwind.config.js file**
```
module.exports = {
  purge: [
    '**/*.cshtml', <-- add this line
  ],
  ...
}
```

This will ensure that none of the Tailwind classes we use in any .cshtml file get purged in our production build.

---

To use Tailwind classes we must add the following lines to our `site.css` in `wwwroot/css`

**wwwroot/css/site.css**
```
@tailwind base;
@tailwind components;
@tailwind utilities;

...
```

---

We can now add scripts that will build these styles do they can be used on our pages:

**package.json**
```
  ...
  "scripts": {
    ...
    "css:build": "postcss ./wwwroot/css/site.css -o ./wwwroot/css/dist.css",
    "css:watch": "postcss ./wwwroot/css/site.css -o ./wwwroot/css/dist.css --watch"
  },
  ...
```

`css:build` will build our styles once, while `css:watch` will rebuild them every time the `site.css` file is changed

_Try running `css:build` and check it creates the `./wwwroot/css/dist.css` file_

---

Now that we have built the `dist.css` file, we need to use it! In `Pages/Shared/_Layout.cshtml`, replace `site.css` with `dist.css`:

**Pages/Shared/_Layout.cshtml**
```
    - <link rel="stylesheet" href="~/css/site.css" />
    + <link rel="stylesheet" href="~/css/dist.css" />
```

_You may want to add `wwwroot/css/dist.css` to your `.gitignore`

---

To ensure our `dist.css` is built when we build our project, we need to add a target to our `.csproj` file:

**TailwindWebApp.csproj**
```
	<Target Name="Tailwind" BeforeTargets="Build">
		<Exec Condition="$(Configuration) == 'Debug'" Command="npm run css:build" />
		<Exec Condition="$(Configuration) == 'Release'" Command="npm run css:build -- --env production" />
	</Target>
```

This will run our `css:build` command before each build. When we do a release build, we run the script with the `--env production` flag, which will purge all unused styles.

---

We need to make another addition to our `.csproj` file to ensure the previous target is run when we change any of our Tailwind files:

```
	<ItemGroup>
		<UpToDateCheckInput Include="wwwroot/css/site.css" Set="Styles" />
		<UpToDateCheckInput Include="postcss.config.js" Set="Styles" />
		<UpToDateCheckInput Include="tailwind.config.js" Set="Styles" />
		<UpToDateCheckOutput Include="wwwroot/css/dist.css" Set="Styles" />
	</ItemGroup>
```

This will check that `wwwroot/css/dist.css` has been built up to date with the last modifications to our `site.css`, `postcss.config.js` and `tailwind.config.js` files.

---

Once last thing to note is that because the styles are only built on each build, they won't be updated if we change without a rebuild.
To get around this, you can run `npm run css:watch` in another terminal to rebuild the `dist.css` file any time you change the `site.css` file.

---

I've created an example project here: https://github.com/GregLahaye/TailwindWebApp
You can view the commit history to see changes made setting up Tailwind.


