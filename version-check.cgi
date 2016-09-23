#!/usr/bin/env ruby
#
# Credentials are taken from the default ENV variables,
# e.g. OCTOKIT_ACCESS_TOKEN.

require 'octokit'
require 'base64'
require 'logger'

logger = Logger.new(STDERR)
logger.level = Logger::INFO

repo = ARGV[0]
base_ref = ARGV[1]
head_ref = ARGV[2]

def get_contents(repo, ref, path)
    response = Octokit.contents(repo, :ref => ref, :path => path)
    return Base64.decode64(response['content'])
end

# Returns an array of three integers
def get_version(repo, ref)
    version_sbt = get_contents(repo, ref, 'version.sbt')
    m = /"(\d+)\.(\d+)\.(\d+)"/.match(version_sbt)
    return m[1].to_i, m[2].to_i, m[3].to_i
end

b = get_version(repo, base_ref)
h = get_version(repo, head_ref)

logger.info("Base version: #{b.join('.')}")
logger.info("Head version: #{h.join('.')}")

if b == h
    logger.info("No version bump")
elsif b[0] == h[0] && b[1] == h[1] && b[2]+1 == h[2]
    logger.info("Third component bump")
elsif b[0] == h[0] && b[1]+1 == h[1] && h[2] == 0
    logger.info("Second component bump")
elsif b[0]+1 == h[0] && h[1] == 0 && h[2] == 0
    logger.info("First component bump")
else
    logger.error("Invalid version change")
end
