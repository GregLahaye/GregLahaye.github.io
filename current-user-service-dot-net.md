# Get the Current User in .NET 5

_In this tutorial we will be creating a simple service and using dependency injection to produce a reuseable way of accessing the current user in .NET 5_

---

Create _Services_ folder in the root of your project&ndash; this is where our service definition and implementation will be stored.

---

Define a _ICurrentUserService_ interface in the _Services_ folder called, this will contain the definition of our method to get the current user:

**Services/ICurrentUserService.cs**

```
namespace Bakery.Services
{
    public interface ICurrentUserService
    {
        Task<IdentityUser> GetCurrentUserAsync();
    }
}
```

---

Let's implement the interface, this is the where the logic to get the current user will lie:

**Services/CurrentUserService.cs**

```
namespace Bakery.Services
{
    public class CurrentUserService : ICurrentUserService
    {
        private readonly IHttpContextAccessor _httpContextAccessor;
        private readonly UserManager<IdentityUser> _userManager;

        public CurrentUserService(
            IHttpContextAccessor httpContextAccessor,
            UserManager<IdentityUser> userManager,
            )
        {
            _httpContextAccessor = httpContextAccessor;
            _userManager = userManager;
        }

        public async Task<IdentityUser> GetCurrentUserAsync()
        {
            return await _userManager.GetUserAsync(_httpContextAccessor.HttpContext.User);
        }
    }

}
```

This is a simple service that will use UserManger to get the IdentityUser from the current HTTP context, however there are still a couple of steps before we can use it.

---

The HTTPContext cannot be accessed in a service by default but thankfully there is a simple line we add to our _Startup.cs_ to allow us to use the HttpContextAccessor

**Startup.cs**

```
        public void ConfigureServices(IServiceCollection services)
        {
            ...
            services.AddHttpContextAccessor();
        }
```

---

We're ready to register our service, this will allow us to use make use of dependency injection to use the service in our pages.

**Startup.cs**

```
        public void ConfigureServices(IServiceCollection services)
        {
            ...
            services.AddTransient<ICurrentUserService, CurrentUserService>();
        }
```

---

Done! The CurrentUserService is ready to be used, here's an example of how we can make use of dependency injection to access our service and get the current user.

```
namespace Bakery.Pages
{
    public class IndexModel : PageModel
    {
        private readonly ICurrentUserService _currentUserService;

        public IndexModel(ICurrentUserService currentUserService)
        {
            _currentUserService = currentUserService;
        }

        public Task<IActionResult> OnGetAsync()
        {
            var user = await _currentUserService.GetCurrentUser();
            ViewData["UserId"] = user.Id;
            return Page();
        }
    }
}
```

_Note:_ be careful to specify the interface, not the implementation, of the service (you want ICurrentUserService, not CurrentUserService)

---

That's it! Hope you found this tutorial useful.
