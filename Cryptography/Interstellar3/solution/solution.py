from Crypto.Util.number import long_to_bytes, bytes_to_long
from sympy import symbols, gcd, Poly
from sympy.polys.domains import GF

n = 0x9146c853fd92be93e3898eb182874ebb3825d0684f73e81747ff99326dce4fed1192813e126b4de8797ceb2eb3d7961c393aca6b57b905e574b7abecb0d5a28708144d40991ab98d74a250c845fbbe9fa6c73ba564959d6f9c804f6903fc39669d424ed753093d1c6a4e4f3ab93a4a021ad6171861eb87f65eaba4cc76af5de5b091e8aad7eb128d3c147eb5778739df422af97d64e7ecb6804f326529944443106b676d496b86735e911991a060b02e362f78457c7c160216dc9ed46665905aa83788585c4d2e6923f4b4b948b3db093d9ea4ccc01d71428e8296c88bd7e0b444d10d1c055f4938225f59a153b38e2beca93d3412a7ad542c5ccff07dd7240d
e = 0x11

p1 = [int(a,16) for a in ['0x6d4e0d8b0d6b7b8dfa69de4b7538737586516f9d0cd2a3200dabbdc8ce0bde5a205cc0146617b29ec57a2a647d080edaa173bb8797cadbde6436686ed9570d5c770bc69de27845f90850d91ece3012dd4b1ca185dc0299a6048bb57bc1072204fc80d953900df2fe0b4ef5183b491c97f64833524df3cb9e3a38e1a910746ebefb7fb3183b9d7c541f10ca27391c079a1746f71f24e374ebd102b7c33e37592e00ec056c356230520b05780a3e50d64c902b73aba714fbbdf1a621143cbc23f7ac7453014c3f777a138c515424b49658b13da74c87d0408dac46521d4fd8d6f7b39590ec3659d0fbf62977d4cc82df9709ad43e07e130419d8b0b14ceff9fe65', '0xcd873b9220616a3c1759fecd2597fa7b295d9ebb6d884550126d5101a6e054c09d313f1b0e7bd4a76ee5fb2adbeb3732341e56d46f76bdce65845b573b3eb746dcabf53334d29f8b0ea941dedf0461c9748e312b877ded26d5147fabe13e30d1c53d07b0c96a690ba67a31fd6e9cce7be12653df9430d5752b8f220b009468126e5a770690670dbd31024584be94f31866bf9898cb67b27e8467e29779eb011deaf5e401f6263df28e97b8c7eb729a25208258ca8ddfc2c7a9fae1e901e6097e30c80aaebafd1b4c8a3c324e12544fbe5b036de09608de6b349bddd0f9c74d4ae5a19e400e20d751571d0ccacec6861c797b068b5d06a6d17653ad975e474d0', '0x414f309a130edd446b67d2573b6b56c60b925f08a6585b009bebe451a7b74446fc98c1d683b0421792ed6b559d221852380a16d8136e3ae2f915ce4f5137d16e692715687363b9d43a5560d921f7a607207406932d04946c66de4f7a7e687828a794822faf5585074cdd4fda84626a2b8a049a318106949332983cc1facb2095c0c85a1f0c8953bd3ef5f266042334fd55c9570e09c19651c341903e771f834493b11a40b4b8fc2de8c206cc6448be5e1b937233ff59f89b8f3c1a2d92ea604a96935a208a63ab00237701d12ac77031cfa696a9fbaceab9bacde906e19932cf9326d94c78149774779b12b860fdb86e013af434a90009a5b6fb4843932fd1fd', '0x439e340fb485b3a4471ccc3650872ab1e8783245b42c7e5c545f1dfbc04069dbe02d69cd150b1ae1b03ea8044ac1dbaf27242cb4912c2c3f3730a8db8683c8956bd21ec3c580f1e5975103bf216a47e538f2d93b6ee948ce0d4b7b5d4f3a9ee54c288d8d3bb9927634b84448f013510b558345a78f5bd8891ad68942361bf9eb656dfdf70ac85b7bd835073fdc396d4656d62ea819e2e24745e52a33387caf0c7831c52819fa2e01465241e66d655dba455164fb2d0a2ce0c348f559f4e96089d117d5a90c678c08501f4ac5fdff27fa69bcb1df666a9369ce7ae777f675c013e6206e8c46a88f30992303782a094845bfc7c7a438a54701aa8f0214d5ea397a', '0x38a06c90b572fafdd27e5722cf978c1c4c89ca8227a501378467817631838981f0bde40fbee3a202ebdeeb605489b1330a9e4a0e8ec874786c8d5816b15b5ed0a173c9c203f068f570f97e903bea7e1761f19f1d47adb3c2e1e31dfefb55f8814c4b944d61f24b5e16d2706729a2007dd2b6c27ae54eb3426ff6206a05ad32961e01eaf7c711f91e8b9b153b19af9be25675363e7384f88dd1e039e633576d4acb40619bd7412d0ade34521fa312c7106499251cdafcc2a04715ce3f1c4d00af997ae2bfa18465026cf2684e970658cd057f966229a3037469bbd2f471714845a6d334153fdf831fa3c8000ba8d420d288c39402eb48d1aece35138b7012cbce', '0x2b058388e06a6773ddda53265e05954d8680126abf9f9f9ac382e7892e87f294ed78ffadbc2f8a546b7f9fd239f4453e7054e1c2425d70fdf58bf5bf25af88293f7a6e4051a780b533202f90ddc5d2f916afe3f85f9512eca4fb37e78424f3e8e98afa4917147c186458e17378fc779566cdac34bf8ed2afae191f8572ccdaad35733ad252579c7d200bd8cc5a159eea80ac9f97916110d86fcceccf3826a7c4887c9efc126868d8a2019955cc997ce1a5142c88c4c065b465b8a52491328beff310b30939d725454642963080a4d895818ce34b055a1b205b217a8036d73a4cc891db0238defe3034195f07a9dee26762fd6c5ce7f6674bc596ca2b9bda1dcb']]
c1 = bytes.fromhex('0929eb99b583c3391020fd41be1f958d53e75c7ba35f6ae9c47d8bc4702ffc9d9d6e1a5d1638db686957f147638df362d1558dbc53efb9963e720bf6b23f2e9520133a6ff5f9936087a806deaa4eb586098f332da8f09566e1792bd3c54969f076e74e4ee6412614dd8f65a2cdebf308af11384ef2bab762fe27211519ccb289f8a4ac1f92d303745966b17a8996d09395f233969774cddbe9e07817509ce33f4b4d9d04783944e4527cdf80805893835bbe1739372d7d6f228b5cf143466b7e4f0696a80edfc87b84e3133d247a6fa9bb0d0a926f7d2f3ec327b870c21f38c52ce28d437e70de35f76fab6a139316c04b9f9e5e23aee20824d3d33259db01c7')

p2 = [int(a,16) for a in ['0x29d21361aac0156cee266347ca9fedc2cf0f4a17a03ddca02b0f4a7174bb80b2aedc8ccda5857e693a5acf42166f2acd7b10fee69116d8520d2303b84bbbec3c4991673360f563ce42f5cb79e1076b4301cc48fb0de0b5fe85f1a1a52160eb04f699b6235414bffc08c75d34f7c21cb2dff57c72ee21a4fe6de3d5c481e53e107e456b84c225428295da8c74a94e822517aa3a91f5813fc6e1761b106c62cd8d6fc5e1a3c4ec86312aea1d54f04feb0e714fa9c18af2dade83f818388fdb8213888b0d552e821b83918466d8cf69b3d256b466a3f664be9e50a7717dbe909d97bd036934a1b941d58c2bcb96f2cf661ff906a5a22520b4e3d8caa036b9f6cb55', '0x89ccb464a04e496d0c594213cbfc0045c978d39a0a0fbcc034ca1fd9b6e5e7bf56e00222788bf12490f4484188259925f47876d5e671d0ec9b7e455dd4158852748f53074dbdbfdbd8e1adbf4ae99cbe24694fc7c094d1ed2f4490f585ba570b7b88796be1a8dcae46b2dfbe51f09777e538563e202e819b2a204db3f3809ff1ed0062ac3b6061f0b2bd06e0d707f96f0da1a88fe220f26853cacd2a8abe332341120d981c6499df6771d7e4db7c1c812f214e3396970ef80a3f574d90246ab7ab911ea6e5b9e5e85ba5a11b939829b4a8caa94b7c608932eeaf3c5b586be4f6895d17cbfdd11c79436d575efec4f642e96655e8652897f721488ca9c7b0eb9e', '0x6330bbb13bb9cac68af2bc6cf79b9177dd234457ad35f43f95d3df037b409c1abf11318b7d0d18af1d46f749d18226d0c1fca6a2964981b5a1b120e49980525ac1e345cf728ce2fbee0282df57d2a268f7c2afb9ae49037a92c29476fd6633958632ad14f947a33f05bdc139531d2c6b0d358ebd07aced356c2450a881b0f9e1b7cbba9a1b2f4cd49eceb4e3a9a138e2b5ffbbdb1d9f44b7c5e872e102cbf84d08004709231f4d6fab9705b3d38d5bf656c523e49bce0769a465a3b14ba342043e4f81bd22e52b4e7de395a5e279e07a2b6e10db1678e4c97a09a67a930577b4a6378ff52d572e3d6d3b502eca0001aae6d621f8a6059ab92c59e9bd6d83622f', '0x5c0d39b4fd34c8152832b66d73275af0f0eaa0b44bd236f02097cf5a65437015a59a4936ee2014f1a39d68772e2a80d08f51ddc9c84a12737466f8422a92f184eaaf3178d24f7037ce4e21f3f93259af7ac4d655d3a288f7a70596b6d7352d34c6c05a0d2198640e4b77541ea9f4dff2f4447f855ee43d4e40639152fe359fd861e4a420f2d903dcd0efa9d1549cbd257246e619708847e86ec5178869d381c48e82a0d63bbad7475964ebb4855e0a60e5bffdb6de6045923a3627d44f7fe2e21c74d0b4f39948e0598bc461f759c6e83fc7541483488d648c8608940719deed4ce5c025b401012936e72ae1be47e42a4f080dd05313ddc6f0a45c8c1530a7dc', '0x33a8937b8120bdb9e82e5307a1ac1b9274b1dd818aae906f1a05caf4192d904c756aecfd8a04f943cc8409da2dad2c2b0ca3c879adfebfbd17cc0201b4f7143867c163a93f70e5ba0032b21b76cb61ce325ca64dbbd3b832eceab1c9f22e74f0bc0a9113aebe3674bfbfa59266aab428287feaa684dc0d97dc409a1d432bb3cd711ab726a844e40eacd6f474683aa31054afb532a87837c7d975f8a8200d2cf10b4a97ab3db8df6fedb33850c6eefa4314d76f2514bff2a81260f50ab94dafefb8dab60d4ede8e3c7dc2821c281a453b4d230d4057ebdff420b4b336130207f730babb6c92843a0a849b5400b94a8899a4d5e4dc0c467ca3eb82fbd05edecab6', '0x1af805e9ad9d6da5d85be69fce8bb78d56ab77f2c678734c1f7d65bb2aafa7e376c10eb3ab8ab42f250a440e06784f9fbe2c5b336058b74d9746c9a87d388a9c95fc9214c08de236c6c6263f571404eafdd73af5a7710b7461fa8cf97df9bde9a84983883225259da73de5e310fc1ed6316c561705be19f718e8856882d46deab7de6631fddb2b79c581fea76d83b1d458c0706c5cd9526adb7432c243cf71298b36df15eb69931c47043633a845cb6f5245f72b2570ebba56aa87c83abb2de8bcbb9e4a9bddb6b139afcf04da908d7aa95ba5dbcabc4f07edbf88c2559433758b819f9cebd608fab0b7f02d70352671892ebc74ff7ca5df379a8e3349d477bc']]
c2 = bytes.fromhex('11d9319ea6e64ddc75a239c92447f14a7b2ec5f96f3abfdd380d888ed1584bbbf582cbed09c33560d5893e0bf2a1ef24e8cef7918fe46ca5aa1b2f364105e6f4a37a9f9eeb55bd6218830be06fb593e5dc065491b28031c43b8ea9108fd53c9765e6e91e23f1017dc977cfa23bb86a8141559164552eaa625823e4bc225dbdefb77810de83889a2783d0bedc98cf829d7e4a340d28ed8ec9db4e63a3ddd6b385e047fe790e4b14b62357162fbf58f11da96d3b9afc2d3855ea5bc5c8ae6d072da912a77d107a0c1e183a9a8aa1221a8526338f82c4984fdf99a962816b5cd2cd1614a1e03cebda0809e4a1a0f2545a05d28b5eced4442646c66594959375a97b')

x = symbols('x')
g1 = Poly((sum(coef * x**i for i, coef in enumerate(p1)))**e-bytes_to_long(c1), x, domain=GF(n))
g2 = Poly((sum(coef * x**i for i, coef in enumerate(p2)))**e-bytes_to_long(c2), x, domain=GF(n))

pgcd = gcd(g1,g2)
m = -pgcd.all_coeffs()[-1]
long_to_bytes(m).decode('utf-8')