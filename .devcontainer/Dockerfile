# 基础镜像
FROM osrf/ros:humble-desktop-full

# 用户参数
ARG USERNAME=yutou
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# 防止交互式弹窗
ENV DEBIAN_FRONTEND=noninteractive

# ------------------------------
# 1. 安装核心工具、ROS包、仿真模型和 Fish Shell
#    (合并了 apt-get 以减少镜像层数)
# ------------------------------
RUN apt-get update && \
    apt-get install -y \
        # === 基础工具 ===
        pip \
        wget \
        curl \
        git \
        nano \
        gedit \
        nautilus \
        iputils-ping \
        net-tools \
        # === Nav2 核心 & 仿真依赖 (关键补充) ===
        ros-humble-nav2-bringup \
        ros-humble-navigation2 \
        ros-humble-turtlebot3-gazebo \
        ros-humble-turtlebot3-bringup \
        ros-humble-turtlebot3-msgs \
        # === 其他 ROS 工具 ===
        ros-humble-gazebo-ros-pkgs \
        ros-humble-cartographer \
        ros-humble-cartographer-ros \
        ros-humble-rqt-tf-tree \
        ros-humble-foxglove-bridge \
        ros-humble-robot-state-publisher \
        ros-humble-joint-state-publisher-gui \
        # === 通信中间件 (推荐 Docker 环境使用) ===
        ros-humble-rmw-cyclonedds-cpp \
        # === Shell ===
        fish && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------
# 2. 创建用户并配置权限
# ------------------------------
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    apt-get update && \
    apt-get install -y sudo && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# ------------------------------
# 3. 安装 Fisher 和 bass (针对 Fish Shell)
# ------------------------------
USER $USERNAME
WORKDIR /home/$USERNAME

# 创建 Fish 配置目录
RUN mkdir -p .config/fish/functions && \
    # 使用 GitHub Raw 链接，比 git.io 更稳定
    curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish > .config/fish/functions/fisher.fish

# 安装 bass 插件 (用于支持 bash 脚本)
RUN /usr/bin/fish -c "fisher install edc/bass"

# ------------------------------
# 4. 配置 ROS 环境 & 环境变量
# ------------------------------
ENV ROS_DISTRO=humble
# 默认使用 CycloneDDS (如果不需要可注释掉)
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV ROS_SETUP_BASH="/opt/ros/humble/setup.bash"

# 配置 Bash (作为备用)
RUN echo "source $ROS_SETUP_BASH" >> /home/$USERNAME/.bashrc && \
    # 增加别名方便 source 工作空间
    echo "alias sb='source ~/.bashrc'" >> /home/$USERNAME/.bashrc

# 配置 Fish (主力环境)
# 注意：这里加了检测逻辑，防止 workspace 不存在时报错
RUN echo 'bass source /opt/ros/humble/setup.bash' >> /home/$USERNAME/.config/fish/config.fish && \
    echo 'if test -f ~/ros2_ws/install/setup.bash; bass source ~/ros2_ws/install/setup.bash; end' >> /home/$USERNAME/.config/fish/config.fish && \
    echo 'if test -f /usr/share/gazebo/setup.sh; bass source /usr/share/gazebo/setup.sh; end' >> /home/$USERNAME/.config/fish/config.fish && \
    # 设置 TurtleBot3 模型名称
    echo 'set -x TURTLEBOT3_MODEL waffle' >> /home/$USERNAME/.config/fish/config.fish

# ------------------------------
# 设置工作目录和默认命令
# ------------------------------
WORKDIR /home/$USERNAME
CMD ["/usr/bin/fish"]