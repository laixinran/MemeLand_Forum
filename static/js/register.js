
function bindEmailCaptchaClick() {
     $("#captcha-btn").click(function (event) {

        // $this 代表的是当前按钮的jquery对象
        var $this = $(this);

        event.preventDefault();

        var email = $("input[name='email']").val();

        //要求服务器发送验证码
        $.ajax({
            url: "/auth/captcha/email?email="+email,
            method: "GET",
            success: function (result) {
                var code = result['code'];
                if (code == 200) {
                    // countdown: 60s
                    var countdown = 60;

                    // 开始倒计时之前，取消按钮的点击事件
                    $this.off("click");
                    var timer = setInterval(function() {
                        $this.text(countdown);
                        countdown -= 1;

                        //倒计时结束时执行
                        if (countdown <= 0) {
                            clearInterval(timer);
                            $this.text("Get Code");
                            //倒计时结束 重新执行点击事件
                            bindEmailCaptchaClick();
                        }
                    }, 1000); //1s
                    alert("Email Sent Successfully!");
                } else {
                    alert(result['message'])
                }
            },
            error: function (error) {
                console.log(error);
            }
        })
    });
}


$(function (){
    bindEmailCaptchaClick();
});
