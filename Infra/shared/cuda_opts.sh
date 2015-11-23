NV_DEVICE="/dev/nvidia"
UVM_DEVICE="${NV_DEVICE}-uvm"
CTL_DEVICE="${NV_DEVICE}ctl"

CUDA_VERSION_LABEL="com.nvidia.cuda.version"

NV_BINS_VOLUME="/usr/local/bin"
NV_BINS="nvidia-cuda-mps-control \
         nvidia-cuda-mps-server \
         nvidia-debugdump \
         nvidia-persistenced \
         nvidia-smi"

NV_LIBS_VOLUME="/usr/local/nvidia"
NV_LIBS_CUDA="cuda \
              nvcuvid \
              nvidia-compiler \
              nvidia-encode \
              nvidia-ml"

NV_DOCKER_ARGS=""

__log()
{
    local level="$1"
    local msg="$2"

    printf "[ NVIDIA ] =$level= $msg\n" >&2
}

__image_label()
{
    local image="$1"
    local label="$2"

    echo $( $DOCKER inspect --format="{{index .Config.Labels \"$label\"}}" $image )
}

__nvsmi_query()
{
    local section="$1"
    local gpu_id="$2" # optional
    local cmd="nvidia-smi -q"

    if [ $# -eq 2 ]; then
        cmd="$cmd -i $gpu_id"
    fi
    echo $( $cmd | grep "$section" | awk '{print $4}' )
}

__library_paths()
{
    local lib="$1"

    echo $( ldconfig -p | grep "lib${lib}.so" | awk '{print $4}' )
}

__library_arch()
{
    local lib="$1"

    echo $( file -L $lib | awk '{print $3}' | cut -d- -f1 )
}

__filter_duplicate_paths()
{
    local paths="$1"

    local sums="$( md5sum $paths | sed 's/[^/]*$/ &/' )"
    local uniq="$( echo "$sums" | uniq -u -f2 | awk '{print $2$3}')"
    local dupl="$( echo "$sums" | uniq --all-repeated=separate -f2 \
                                | uniq -w 32 | awk 'NF {print $2$3}')"
    echo $uniq $dupl
}

check_prerequisites()
{
    local cmds="nvidia-smi nvidia-modprobe"

    for cmd in $cmds; do
        command -v $cmd >/dev/null && continue
        __log ERROR "Command not found: $cmd"
        exit 1
    done
}

check_image_version()
{
    local image="$1"
    local driver_version="$( __nvsmi_query "Driver Version" )"
    local cuda_image_version="$( __image_label $image $CUDA_VERSION_LABEL )"

    if [ -z $cuda_image_version ]; then
        __log INFO "Not a CUDA image, nothing to be done"
        return 1
    fi
    __log INFO "Driver version: $driver_version"
    __log INFO "CUDA image version: $cuda_image_version"
    return 0
}

load_uvm()
{
    if [ ! -e $UVM_DEVICE ]; then
        nvidia-modprobe -u -c=0
    fi
}

build_docker_args()
{
    local args="--device=$CTL_DEVICE --device=$UVM_DEVICE"

    for gpu in $( echo $GPU | tr -s ", " " " ); do
        local minor="$( __nvsmi_query "Minor Number" $gpu )"
        if [ -z $minor ]; then
            __log WARN "Could not find GPU device: $gpu"
            continue
        fi
        args="$args --device=${NV_DEVICE}$minor"
    done

    for lib in $NV_LIBS_CUDA; do
        local paths="$( __library_paths $lib )"
        echo $paths
        if [ -z "$paths" ]; then
            __log WARN "Could not find library: $lib"
            continue
        fi
        for path in $( __filter_duplicate_paths "$paths" ); do
            args="$args -v $path:$path"
            case $( __library_arch "$path" ) in
                32) args="$args -v $path:$NV_LIBS_VOLUME/lib/$(basename $path)" ;;
                64) args="$args -v $path:$NV_LIBS_VOLUME/lib64/$(basename $path)" ;;
            esac
        done
    done

    for bin in $NV_BINS; do
        local path="$( which $bin )"
        if [ -z $path ]; then
            __log WARN "Could not find binary: $bin"
            continue
        fi
        args="$args -v $path:$NV_BINS_VOLUME/$bin"
    done

    NV_DOCKER_ARGS=$args
}

build_docker_yaml()
{ 
    local yml = "
devices:
  - ${CTL_DEVICE}:${CTL_DEVICE}
  - ${UVM_DEVICE}:${UVM_DEVICE}
    "

printf -v text "%s" "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed " \
                    "do eiusmod empor incididunt ut labore et dolore magna aliqua. "\
                    "Ut enim ad minim veniam ..."
                    echo $text

    local args="--device=$CTL_DEVICE --device=$UVM_DEVICE"

    for gpu in $( echo $GPU | tr -s ", " " " ); do
        local minor="$( __nvsmi_query "Minor Number" $gpu )"
        if [ -z $minor ]; then
            __log WARN "Could not find GPU device: $gpu"
            continue
        fi
        args="$args --device=${NV_DEVICE}$minor"
    done

    for lib in $NV_LIBS_CUDA; do
        local paths="$( __library_paths $lib )"
        echo $paths
        if [ -z "$paths" ]; then
            __log WARN "Could not find library: $lib"
            continue
        fi
        for path in $( __filter_duplicate_paths "$paths" ); do
            args="$args -v $path:$path"
            case $( __library_arch "$path" ) in
                32) args="$args -v $path:$NV_LIBS_VOLUME/lib/$(basename $path)" ;;
                64) args="$args -v $path:$NV_LIBS_VOLUME/lib64/$(basename $path)" ;;
            esac
        done
    done

    for bin in $NV_BINS; do
        local path="$( which $bin )"
        if [ -z $path ]; then
            __log WARN "Could not find binary: $bin"
            continue
        fi
        args="$args -v $path:$NV_BINS_VOLUME/$bin"
    done

    NV_DOCKER_ARGS=$args
    NV_DOCKER_YML=$yml
}

build_docker_yaml

# echo $NV_DOCKER_ARGS
echo $NV_DOCKER_YML