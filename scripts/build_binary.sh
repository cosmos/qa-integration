#/bin/sh

set -e
source ./env 

REPO=$DAEMON-$CHAIN_VERSION

echo "INFO: Clone the repo $GH_URL into $REPO"
if [ ! -d $REPO ]
then
    git clone -b $CHAIN_VERSION --single-branch $GH_URL $REPO
fi

## Docker 
echo "FROM golang:1.18-alpine AS build-env

# Install minimum necessary dependencies
ENV PACKAGES curl make git libc-dev bash gcc linux-headers eudev-dev python3
RUN apk add --no-cache \$PACKAGES\

RUN go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0

# Set working directory for the build
WORKDIR /project

# Add source files
COPY . .

# install simapp, remove packages
RUN make build

# Final image
FROM alpine:edge

# Install deps 
RUN apk add --update ca-certificates python3 jq bash py-pip py3-setuptools
RUN pip install pymongo
WORKDIR /root


COPY --from=build-env /project/build/$DAEMON /usr/bin/$DAEMON
COPY --from=build-env /go/bin/cosmovisor /usr/bin/cosmovisor

cmd [\"$DAEMON\",\"start\",\"--home\",\"/app\"]" > ${DAEMON}_Dockerfile

echo "INFO: Build the docker images with ${DAEMON}_Dockerfile and version ${CHAIN_VERSION}"

IMAGE=qa$DAEMON$CHAIN_VERSION
if test ! -z "$(docker images -q $IMAGE:latest)"
then 
    echo "INFO: docker image $IMAGE is already exists"
else
    docker build -t $IMAGE -f ./${DAEMON}_Dockerfile ./$REPO
fi

# check version
echo "$DAEMON installed version $(docker run -it --rm $IMAGE $DAEMON version)"
