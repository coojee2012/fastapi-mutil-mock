@RestController
@RequestMapping("/auth")
public class AuthController {
    @Autowired
    private UserService userService;

    @PostMapping("/login")
    public ResponseEntity<TokenResponse> login(@RequestBody LoginRequest loginRequest) {
        User user = userService.findByUsernameAndPassword(loginRequest.getUsername(), loginRequest.getPassword());
        if (user == null) {
            return ResponseEntity.badRequest().build();
        }
        String token = Jwts.builder()
                .setSubject(user.getUsername())
                .setExpiration(new Date(System.currentTimeMillis() + 864000000))
                .signWith(SignatureAlgorithm.HS512, "secret")
                .compact();
        TokenResponse response = new TokenResponse();
        response.setToken(token);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/check")
    public ResponseEntity<UserInfoResponse> check(@RequestHeader("Authorization") String authorization) {
        String token = authorization.replace("Bearer ", "");
        Claims claims = Jwts.parser().setSigningKey("secret").parseClaimsJws(token).getBody();
        String username = claims.getSubject();
        User user = userService.findByUsername(username);
        if (user == null) {
            return ResponseEntity.badRequest().build();
        }
        UserInfoResponse response = new UserInfoResponse();
        response.setUsername(user.getUsername());
        response.setEmail(user.getEmail());
        return ResponseEntity.ok(response);
    }
}

/**
 * 在这个代码示例中，我们定义了两个接口：/auth/login 和 /auth/check。前者用于处理用户登录请求，后者用于验证令牌并返回用户信息。

    该代码示例使用了 JWT 实现令牌的生成和验证，实际使用中你可以根据需求选择合适的令牌机制。
 */

/** 
 服务端验证令牌的有效性通常需要使用 JSON Web Token (JWT)。JWT 是一种基于 JSON 的开放标准，用于在各方之间安全地传递声明（例如用户身份）。

令牌通常包含三个部分：

头部：描述了令牌的类型和签名算法
负载（Payload）：包含了声明（例如用户身份）
签名：对令牌进行签名，以确保不被篡改
在验证令牌时，服务端需要首先验证令牌的签名是否有效，然后检查令牌是否已经过期。可以在 JWT 负载中包含过期时间，然后在服务端检查该时间是否已经过去。

还可以在 JWT 负载中包含用户的角色和权限，然后在服务端检查该用户是否具有访问请求的资源的权限。

具体的实现方式因语言和框架而异，例如，在 Java 中可以使用第三方库如 JJWT 来实现 JWT 的编码和解码。
*/

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;

...

public void checkToken(String token) throws Exception {
  try {
    Claims claims = Jwts.parser()
      .setSigningKey("secret")
      .parseClaimsJws(token
